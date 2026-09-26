#!/usr/bin/env python3
"""Fail-fast preflight for mixed Windows/WSL builds and artifact delivery."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
from typing import Any


WINDOWS_SUFFIXES = (".exe", ".cmd", ".bat", ".ps1")
RUNTIMES = ("node", "npm", "npx", "bun", "python3", "ffmpeg", "ffprobe")
ALLOWED_INLINE_PREFIXES = ("data:", "#", "https://", "http://")


def is_wsl() -> bool:
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        release = Path("/proc/sys/kernel/osrelease").read_text(encoding="utf-8")
    except OSError:
        release = platform.release()
    return "microsoft" in release.lower() or "wsl" in release.lower()


def normalize_input_path(raw: str, under_wsl: bool) -> Path:
    unc = re.match(r"^\\\\wsl(?:\.localhost|\$)?\\[^\\]+\\(.+)$", raw, re.I)
    if unc:
        return Path("/" + unc.group(1).replace("\\", "/")).resolve(strict=False)

    drive = re.match(r"^([A-Za-z]):[\\/](.*)$", raw)
    if drive and under_wsl:
        rest = drive.group(2).replace("\\", "/")
        return Path(f"/mnt/{drive.group(1).lower()}/{rest}").resolve(strict=False)

    path = Path(raw)
    if not path.is_absolute():
        path = Path.cwd() / path
    return path.resolve(strict=False)


def classify_executable(path: str | None) -> str:
    if not path:
        return "missing"
    candidates = (path, os.path.realpath(path))
    for candidate in candidates:
        lowered = candidate.lower().replace("\\", "/")
        if re.match(r"^[a-z]:/", lowered):
            return "windows"
        if re.match(r"^/mnt/[a-z]/", lowered):
            return "windows"
        if lowered.endswith(WINDOWS_SUFFIXES):
            return "windows"
        if "/windows/" in lowered or "/program files/" in lowered:
            return "windows"
    return "linux"


def find_linux_candidate(name: str, node_path: str | None = None) -> str | None:
    candidates: list[Path] = []
    if node_path and classify_executable(node_path) == "linux":
        candidates.append(Path(node_path).resolve().parent / name)
    candidates.extend(
        [
            Path("/home/linuxbrew/.linuxbrew/bin") / name,
            Path("/usr/local/bin") / name,
            Path("/usr/bin") / name,
            Path.home() / ".local/bin" / name,
        ]
    )
    nvm_root = Path.home() / ".nvm/versions/node"
    if nvm_root.is_dir():
        candidates.extend(sorted(nvm_root.glob(f"*/bin/{name}"), reverse=True))
    for candidate in candidates:
        if (
            candidate.is_file()
            and os.access(candidate, os.X_OK)
            and classify_executable(str(candidate)) == "linux"
        ):
            return str(candidate)
    return None


def command_version(path: str, kind: str) -> str | None:
    if kind == "windows" and is_wsl():
        return None
    try:
        proc = subprocess.run(
            [path, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    output = (proc.stdout or proc.stderr).strip().splitlines()
    return output[0] if output else None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def windows_path(path: Path, under_wsl: bool) -> str | None:
    if not under_wsl:
        return str(path)
    wslpath = shutil.which("wslpath")
    if wslpath and classify_executable(wslpath) == "linux":
        try:
            proc = subprocess.run(
                [wslpath, "-w", str(path)],
                check=False,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if proc.returncode == 0 and proc.stdout.strip():
                return proc.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            pass
    match = re.match(r"^/mnt/([a-zA-Z])/(.*)$", str(path))
    if match:
        return f"{match.group(1).upper()}:\\{match.group(2).replace('/', chr(92))}"
    distro = os.environ.get("WSL_DISTRO_NAME", "Ubuntu")
    return f"\\\\wsl.localhost\\{distro}{str(path).replace('/', chr(92))}"


def inspect_html(path: Path, inline: bool, errors: list[str], warnings: list[str]) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        errors.append(f"Cannot read HTML as UTF-8: {path}: {exc}")
        return {}

    dependencies = re.findall(r"\b(?:src|href|poster)\s*=\s*['\"]([^'\"]+)['\"]", text, re.I)
    dependencies.extend(
        value.strip(" '\"")
        for value in re.findall(r"\burl\s*\(([^)]+)\)", text, re.I)
    )
    local_dependencies = [
        value
        for value in dependencies
        if not value.lower().startswith(ALLOWED_INLINE_PREFIXES)
    ]
    external_dependencies = [
        value
        for value in dependencies
        if value.lower().startswith(("https://", "http://"))
    ]
    result = {
        "fragment": not bool(re.search(r"<!doctype|<html\b|<head\b|<body\b", text, re.I)),
        "dependencyCount": len(dependencies),
        "dataDependencyCount": sum(value.lower().startswith("data:") for value in dependencies),
        "externalDependencies": external_dependencies[:8],
        "localDependencies": local_dependencies[:8],
        "dataUriCount": len(re.findall(r"data:(?:image|video)/", text, re.I)),
    }

    if inline:
        if not result["fragment"]:
            errors.append("Inline HTML must be a fragment without doctype/html/head/body tags.")
        if local_dependencies:
            errors.append(
                "Inline HTML contains local or relative dependencies: "
                + ", ".join(local_dependencies[:8])
            )
        if re.search(r"\b(?:fetch|XMLHttpRequest|WebSocket)\s*\(?", text):
            warnings.append("Inline HTML contains a network API; verify the host CSP and skill contract.")
    return result


def inspect_media(path: Path, decode: bool, errors: list[str], warnings: list[str]) -> dict[str, Any]:
    ffprobe = shutil.which("ffprobe")
    if not ffprobe or classify_executable(ffprobe) != "linux" and is_wsl():
        errors.append("A native ffprobe executable is required to inspect media.")
        return {}
    try:
        proc = subprocess.run(
            [
                ffprobe,
                "-v",
                "error",
                "-show_entries",
                "format=duration,size,bit_rate:stream=index,codec_type,codec_name,profile,width,height,pix_fmt,r_frame_rate,color_space,color_transfer,color_primaries",
                "-of",
                "json",
                str(path),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        errors.append(f"ffprobe failed for {path}: {exc}")
        return {}
    if proc.returncode != 0:
        errors.append(f"ffprobe rejected {path}: {proc.stderr.strip()}")
        return {}
    result = json.loads(proc.stdout)

    if decode:
        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg or classify_executable(ffmpeg) != "linux" and is_wsl():
            errors.append("A native ffmpeg executable is required for full decode verification.")
        else:
            decode_proc = subprocess.run(
                [ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"],
                check=False,
                capture_output=True,
                text=True,
            )
            result["fullDecodePassed"] = decode_proc.returncode == 0
            if decode_proc.returncode != 0:
                errors.append(f"Full decode failed for {path}: {decode_proc.stderr.strip()}")
    else:
        warnings.append(f"Media was probed but not fully decoded: {path}")
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=str(Path.cwd()))
    parser.add_argument("--require-linux-runtime", action="append", default=[])
    parser.add_argument("--artifact")
    parser.add_argument("--mirror")
    parser.add_argument("--inline", action="store_true")
    parser.add_argument("--max-inline-bytes", type=int, default=2_000_000)
    parser.add_argument("--media", action="append", default=[])
    parser.add_argument("--decode-media", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    under_wsl = is_wsl()
    workspace = normalize_input_path(args.workspace, under_wsl)
    errors: list[str] = []
    warnings: list[str] = []

    report: dict[str, Any] = {
        "environment": {
            "system": platform.system(),
            "release": platform.release(),
            "isWsl": under_wsl,
        },
        "workspace": {
            "input": args.workspace,
            "linuxPath": str(workspace),
            "windowsPath": windows_path(workspace, under_wsl),
            "exists": workspace.exists(),
        },
        "runtimes": {},
        "artifact": None,
        "mirror": None,
        "media": [],
    }

    node_path = shutil.which("node")
    for name in RUNTIMES:
        selected = shutil.which(name)
        kind = classify_executable(selected)
        candidate = find_linux_candidate(name, node_path)
        item = {
            "selected": selected,
            "resolved": os.path.realpath(selected) if selected else None,
            "kind": kind,
            "version": command_version(selected, kind) if selected else None,
            "linuxCandidate": candidate,
        }
        report["runtimes"][name] = item
        if under_wsl and selected and kind == "windows":
            message = (
                f"WSL selected Windows {name}: {selected}. "
                + (f"Use {candidate}." if candidate else "Install or select a Linux-native runtime.")
            )
            if name in {"node", "npm", "npx", "python3"} or name in args.require_linux_runtime:
                errors.append(message)
            else:
                warnings.append(message)

    for required in args.require_linux_runtime:
        item = report["runtimes"].get(required)
        if item is None:
            errors.append(f"Unknown required runtime: {required}")
        elif item["kind"] != "linux":
            errors.append(f"Required Linux runtime is unavailable or not selected: {required}")

    if not workspace.exists():
        errors.append(f"Workspace does not exist after normalization: {workspace}")

    artifact_path: Path | None = None
    if args.artifact:
        artifact_path = normalize_input_path(args.artifact, under_wsl)
        if not artifact_path.is_file():
            errors.append(f"Artifact is missing or not a file: {artifact_path}")
        else:
            artifact_info: dict[str, Any] = {
                "linuxPath": str(artifact_path),
                "windowsPath": windows_path(artifact_path, under_wsl),
                "bytes": artifact_path.stat().st_size,
                "sha256": sha256(artifact_path),
            }
            if artifact_path.suffix.lower() in {".html", ".htm"}:
                artifact_info["html"] = inspect_html(artifact_path, args.inline, errors, warnings)
            if args.inline and artifact_info["bytes"] >= args.max_inline_bytes:
                errors.append(
                    f"Inline artifact is {artifact_info['bytes']} bytes; limit is below {args.max_inline_bytes} bytes."
                )
            report["artifact"] = artifact_info

    if args.inline and not args.mirror:
        errors.append("Inline mixed-path delivery requires --mirror for byte-identity proof.")

    if args.mirror:
        mirror_path = normalize_input_path(args.mirror, under_wsl)
        if not mirror_path.is_file():
            errors.append(f"Mirror is missing or not a file: {mirror_path}")
        else:
            mirror_info = {
                "linuxPath": str(mirror_path),
                "windowsPath": windows_path(mirror_path, under_wsl),
                "bytes": mirror_path.stat().st_size,
                "sha256": sha256(mirror_path),
            }
            report["mirror"] = mirror_info
            if report["artifact"] and mirror_info["sha256"] != report["artifact"]["sha256"]:
                errors.append("Artifact and mirror SHA-256 hashes differ.")

    for raw_media in args.media:
        media_path = normalize_input_path(raw_media, under_wsl)
        if not media_path.is_file():
            errors.append(f"Media is missing or not a file: {media_path}")
            continue
        report["media"].append(
            {
                "linuxPath": str(media_path),
                "windowsPath": windows_path(media_path, under_wsl),
                "bytes": media_path.stat().st_size,
                "sha256": sha256(media_path),
                "probe": inspect_media(media_path, args.decode_media, errors, warnings),
            }
        )

    report["browserVerificationRequired"] = bool(args.inline or args.media or args.artifact)
    report["errors"] = list(dict.fromkeys(errors))
    report["warnings"] = list(dict.fromkeys(warnings))
    report["ok"] = not report["errors"]

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{'PASS' if report['ok'] else 'FAIL'} mixed Windows/WSL preflight")
        print(f"workspace linux:   {report['workspace']['linuxPath']}")
        print(f"workspace windows: {report['workspace']['windowsPath']}")
        for name, item in report["runtimes"].items():
            selected = item["selected"] or "missing"
            print(f"runtime {name:8} {item['kind']:7} {selected}")
        if report["artifact"]:
            print(f"artifact sha256:   {report['artifact']['sha256']}")
        if report["mirror"]:
            print(f"mirror sha256:     {report['mirror']['sha256']}")
        for error in report["errors"]:
            print(f"ERROR: {error}", file=sys.stderr)
        for warning in report["warnings"]:
            print(f"WARN: {warning}", file=sys.stderr)
        if report["browserVerificationRequired"]:
            print("NEXT: verify the actual browser/Codex surface; preflight is not rendering proof.")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
