#!/usr/bin/env python3
"""Install the pinned skill set from this bundle into an explicit user skill directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
MANIFEST = PACKAGE / 'manifest.json'


def fail(message: str) -> None:
    raise SystemExit(message)


def safe_relative(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or any(part in {'..', '.'} for part in path.parts):
        fail(f'Unsafe manifest path: {value}')
    return path


def safe_name(value: str) -> str:
    path = safe_relative(value)
    if len(path.parts) != 1 or path.name != value:
        fail(f'Unsafe skill name: {value}')
    return value


def content_hash(folder: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(folder.rglob('*')):
        if file.is_file():
            digest.update(file.relative_to(folder).as_posix().encode())
            digest.update(b'\0')
            digest.update(file.read_bytes())
    return digest.hexdigest()


def command(*args: str) -> str:
    proc = subprocess.run(args, text=True, capture_output=True)
    if proc.returncode:
        fail(f'Command failed: {" ".join(args[:3])}\n{proc.stderr.strip()}')
    return proc.stdout.strip()


def check_links(folder: Path, root: Path) -> None:
    resolved_root = root.resolve()
    for path in folder.rglob('*'):
        if path.is_symlink() and not path.resolve().is_relative_to(resolved_root):
            fail(f'Symlink escapes source checkout: {path}')


def prepare_repo(repo: str, source: dict, paths: list[str], staging: Path) -> Path:
    if not repo or '/' not in repo or source['url'] != f'https://github.com/{repo}.git':
        fail(f'Unexpected GitHub source: {repo}')
    dest = staging / 'repos' / repo.replace('/', '-')
    dest.parent.mkdir(parents=True, exist_ok=True)
    command('git', 'clone', '--quiet', '--depth', '1', '--filter=blob:none', '--no-checkout', source['url'], str(dest))
    commit = source['commit']
    if command('git', '-C', str(dest), 'rev-parse', 'HEAD') != commit:
        command('git', '-C', str(dest), 'fetch', '--quiet', '--depth', '1', 'origin', commit)
    command('git', '-C', str(dest), 'sparse-checkout', 'set', '--cone', *paths)
    command('git', '-C', str(dest), 'checkout', '--quiet', '--detach', commit)
    if command('git', '-C', str(dest), 'rev-parse', 'HEAD') != commit:
        fail(f'Commit mismatch for {repo}')
    return dest


def stage_items(items: list[dict], manifest: dict, staging: Path) -> Path:
    prepared = staging / 'prepared'
    prepared.mkdir()
    groups: dict[str, list[dict]] = {}
    for item in items:
        if 'repo' in item:
            groups.setdefault(item['repo'], []).append(item)
        else:
            source = PACKAGE / safe_relative(item['bundle_path'])
            if content_hash(source) != item['content_sha256']:
                fail(f'Bundled content hash mismatch: {item["name"]}')
            shutil.copytree(source, prepared / item['name'])
    for repo, members in groups.items():
        paths = sorted({str(safe_relative(member['path'])) for member in members})
        source = prepare_repo(repo, manifest['sources'][repo], paths, staging)
        for member in members:
            path = str(safe_relative(member['path']))
            tree = command('git', '-C', str(source), 'ls-tree', manifest['sources'][repo]['commit'], '--', path)
            if not tree or tree.split()[2] != member['tree_sha']:
                fail(f'Git tree mismatch: {repo}/{path}')
            folder = source / path
            if not (folder / 'SKILL.md').is_file():
                fail(f'Missing SKILL.md: {repo}/{path}')
            check_links(folder, source)
            shutil.copytree(folder, prepared / member['name'])
    for item in items:
        if not (prepared / item['name'] / 'SKILL.md').is_file():
            fail(f'Staged skill missing SKILL.md: {item["name"]}')
    return prepared


def install(items: list[dict], manifest: dict, target: Path) -> Path:
    target = target.expanduser().resolve()
    if target.name != 'skills':
        fail('Target must be the skills directory itself, such as ~/.agents/skills')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='skill-fetch-') as temporary:
        prepared = stage_items(items, manifest, Path(temporary))
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        backup = target.parent / 'skill-backups' / stamp
        if backup.exists():
            fail(f'Backup already exists: {backup}')
        (backup / 'old').mkdir(parents=True)
        (backup / 'after-rollback').mkdir()
        receipt = {'target': str(target), 'generated_on': manifest['generated_on'],
                   'names': [item['name'] for item in items], 'previously_present': []}
        target.mkdir(parents=True, exist_ok=True)
        installed: list[str] = []
        try:
            for item in items:
                name = item['name']
                current = target / name
                installed.append(name)
                if current.exists() or current.is_symlink():
                    receipt['previously_present'].append(name)
                    shutil.move(str(current), str(backup / 'old' / name))
                shutil.copytree(prepared / name, current)
            (backup / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        except Exception:
            for name in reversed(installed):
                current = target / name
                if current.exists():
                    shutil.move(str(current), str(backup / 'after-rollback' / name))
                old = backup / 'old' / name
                if old.exists() or old.is_symlink():
                    shutil.move(str(old), str(current))
            raise
        return backup


def rollback(receipt_path: Path) -> None:
    receipt_path = receipt_path.expanduser().resolve()
    receipt = json.loads(receipt_path.read_text())
    target = Path(receipt['target'])
    backup = receipt_path.parent
    for name in reversed(receipt['names']):
        current = target / name
        if current.exists() or current.is_symlink():
            archive = backup / 'after-rollback' / name
            if archive.exists():
                fail(f'Rollback archive exists: {archive}')
            shutil.move(str(current), str(archive))
        old = backup / 'old' / name
        if old.exists() or old.is_symlink():
            shutil.move(str(old), str(current))
    print(f'Restored prior skill set. Updated copies retained under {backup / "after-rollback"}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, help='Explicit Codex user skills directory, e.g. ~/.agents/skills')
    parser.add_argument('--install', action='store_true', help='Fetch and install the pinned skills')
    parser.add_argument('--only', nargs='+', help='Skill names to include (default: all)')
    parser.add_argument('--scope', choices=['codex', 'windows_agents', 'wsl_agents'],
                        help='Install only skills discovered in this original location')
    parser.add_argument('--rollback', type=Path, help='Path to a prior receipt.json')
    parser.add_argument('--check-updates', action='store_true', help='Read current GitHub heads without changing files')
    args = parser.parse_args()
    if args.rollback:
        rollback(args.rollback)
        return
    manifest = json.loads(MANIFEST.read_text())
    if manifest['schema_version'] != 1:
        fail('Unsupported manifest schema')
    all_names = [safe_name(item['name']) for item in manifest['skills']]
    if len(all_names) != len(set(all_names)):
        fail('Duplicate skill names in manifest')
    if args.check_updates:
        for repo, source in manifest['sources'].items():
            result = command('git', 'ls-remote', source['url'], 'HEAD').split()[0]
            state = 'pinned-current' if result == source['commit'] else 'new-head-available'
            print(f'{repo}: {state} ({source["commit"][:7]} -> {result[:7]})')
        return
    items = manifest['skills']
    if args.scope:
        items = [item for item in items if args.scope in item['discovered_in']]
    if args.only:
        names = set(args.only)
        items = [item for item in items if item['name'] in names]
        unknown = names - {item['name'] for item in items}
        if unknown:
            fail(f'Unknown skills: {", ".join(sorted(unknown))}')
    print(f'{len(items)} skills selected: {sum("repo" in x for x in items)} pinned GitHub, '
          f'{sum("bundle_path" in x for x in items)} bundled. '
          f'{len(manifest["remote_plugins"])} plugins are listed separately.')
    if args.target:
        target = args.target.expanduser().resolve()
        print(f'Target: {target} ({sum((target / item["name"]).exists() for item in items)} existing names would be backed up)')
        if not args.install:
            create = [item['name'] for item in items if not (target / item['name']).exists()]
            replace = [item['name'] for item in items if (target / item['name']).exists()]
            print('Create: ' + (', '.join(create) or '(none)'))
            print('Replace after backup: ' + (', '.join(replace) or '(none)'))
    if not args.install:
        print('Preview only. Add --install and --target to apply.')
        return
    if not args.target:
        fail('--install requires --target')
    backup = install(items, manifest, args.target)
    print(f'Installed {len(items)} skills. Backup and rollback receipt: {backup / "receipt.json"}')


if __name__ == '__main__':
    main()
