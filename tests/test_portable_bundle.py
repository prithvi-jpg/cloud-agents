from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
PORTABLE = ROOT / "portable"
ARCHIVE = ROOT / "downloads" / "skill-portability-pack.zip"


def bundled_hash(folder: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(folder.rglob("*")):
        if file.is_file():
            digest.update(file.relative_to(folder).as_posix().encode())
            digest.update(b"\0")
            digest.update(file.read_bytes())
    return digest.hexdigest()


def archive_differences(archive: Path, source: Path) -> list[str]:
    expected = {
        (Path("skill-portability-pack") / file.relative_to(source)).as_posix(): file.read_bytes()
        for file in source.rglob("*")
        if file.is_file() and "__pycache__" not in file.parts and file.suffix != ".pyc"
    }
    with ZipFile(archive) as package:
        actual = {name: package.read(name) for name in package.namelist() if not name.endswith("/")}
    return sorted(name for name in expected.keys() | actual.keys()
                  if expected.get(name) != actual.get(name))


class PortableBundleTests(unittest.TestCase):
    def test_manifest_has_complete_pinned_sources_and_valid_custom_content(self) -> None:
        manifest = json.loads((PORTABLE / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        skills = manifest["skills"]
        self.assertEqual(len(skills), 189)
        self.assertEqual(len({item["name"] for item in skills}), len(skills))
        self.assertEqual(sum("repo" in item for item in skills), 168)
        self.assertEqual(sum("bundle_path" in item for item in skills), 21)
        self.assertEqual(len(manifest["sources"]), 18)
        self.assertEqual(len(manifest["remote_plugins"]), 31)
        for item in skills:
            self.assertTrue(item["name"])
            self.assertEqual(Path(item["name"]).name, item["name"])
            if "repo" in item:
                source = manifest["sources"][item["repo"]]
                self.assertEqual(source["url"], f'https://github.com/{item["repo"]}.git')
                self.assertEqual(len(source["commit"]), 40)
                self.assertEqual(len(item["tree_sha"]), 40)
            else:
                folder = PORTABLE / item["bundle_path"]
                self.assertTrue((folder / "SKILL.md").is_file())
                self.assertEqual(bundled_hash(folder), item["content_sha256"])

    def test_zip_matches_reviewable_portable_directory(self) -> None:
        with ZipFile(ARCHIVE) as package:
            self.assertIsNone(package.testzip())
        self.assertEqual(archive_differences(ARCHIVE, PORTABLE), [])

    def test_zip_check_rejects_a_tampered_file(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            corrupted = Path(temporary) / "corrupted.zip"
            with ZipFile(ARCHIVE) as original, ZipFile(corrupted, "w") as edited:
                for name in original.namelist():
                    data = original.read(name)
                    if name == "skill-portability-pack/README.md":
                        data += b"\nUnexpected edit.\n"
                    edited.writestr(name, data)
            self.assertIn("skill-portability-pack/README.md",
                          archive_differences(corrupted, PORTABLE))


if __name__ == "__main__":
    unittest.main()
