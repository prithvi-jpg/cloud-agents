from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill" / "adaptive-agent-operating-system"
SCRIPTS = SKILL / "scripts"
SCHEMAS = SKILL / "assets" / "schemas"


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class ProjectSpineTests(unittest.TestCase):
    def test_initializer_creates_and_preserves_project_spine(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first = run_script(
                "init_project.py",
                "--root",
                str(root),
                "--name",
                "Fixture",
                "--outcome",
                "Verify a bounded workflow.",
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            receipt = json.loads(first.stdout)
            self.assertEqual(
                {item["status"] for item in receipt["files"]}, {"created"}
            )

            state = root / "docs" / "agent" / "STATE.md"
            state.write_text(state.read_text(encoding="utf-8") + "\nMaintainer edit.\n", encoding="utf-8")

            second = run_script(
                "init_project.py",
                "--root",
                str(root),
                "--name",
                "Fixture",
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            receipt = json.loads(second.stdout)
            self.assertEqual(
                {item["status"] for item in receipt["files"]}, {"skipped_existing"}
            )
            self.assertIn("Maintainer edit.", state.read_text(encoding="utf-8"))

            validation = run_script("validate_project.py", "--root", str(root))
            self.assertEqual(validation.returncode, 0, validation.stdout)
            self.assertTrue(json.loads(validation.stdout)["ok"])

    def test_validator_rejects_missing_spine(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = run_script("validate_project.py", "--root", temporary)
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertEqual(len(payload["errors"]), 3)

    def test_repository_validates_its_own_spine(self) -> None:
        result = run_script("validate_project.py", "--root", str(ROOT))
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(json.loads(result.stdout)["ok"])


class SchemaTests(unittest.TestCase):
    def test_schemas_are_json_with_unique_canonical_ids(self) -> None:
        ids: set[str] = set()
        files = sorted(SCHEMAS.glob("*.json"))
        self.assertGreaterEqual(len(files), 5)
        for path in files:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["$schema"], "https://json-schema.org/draft/2020-12/schema")
            schema_id = payload["$id"]
            self.assertTrue(
                schema_id.startswith(
                    "https://raw.githubusercontent.com/prithvi-jpg/cloud-agents/main/skill/adaptive-agent-operating-system/"
                )
            )
            self.assertNotIn(schema_id, ids)
            ids.add(schema_id)
            self.assertTrue(payload.get("required"))


class SkillPackageTests(unittest.TestCase):
    def test_skill_frontmatter_matches_package_name(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        _, frontmatter, _ = text.split("---", 2)
        fields = {
            key.strip(): value.strip()
            for line in frontmatter.strip().splitlines()
            for key, value in [line.split(":", 1)]
        }
        self.assertEqual(set(fields), {"name", "description"})
        self.assertEqual(fields["name"], SKILL.name)
        self.assertIn("bounded autonomous execution", fields["description"])
        self.assertLess(len(text.splitlines()), 500)

    def test_openai_metadata_targets_the_skill(self) -> None:
        metadata = (SKILL / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "Agent Systems Foundry OS"', metadata)
        self.assertIn("$adaptive-agent-operating-system", metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)


class MemoryBundleTests(unittest.TestCase):
    def test_memory_validator_accepts_valid_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            record = Path(temporary) / "decision.md"
            record.write_text(
                """---
id: decision.example-001
type: decision
scope: test
status: active
created_at: 2026-08-03T00:00:00Z
updated_at: 2026-08-03T00:00:00Z
source_refs: [\"test:fixture\"]
confidence: confirmed
privacy: public
tags: [\"test\"]
related: []
supersedes: []
stale_after: null
---
The validator keeps provenance and privacy explicit.
""",
                encoding="utf-8",
            )
            result = run_script("validate_memory_bundle.py", "--root", temporary)
            self.assertEqual(result.returncode, 0, result.stdout)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["records"], 1)

    def test_memory_validator_rejects_empty_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result = run_script("validate_memory_bundle.py", "--root", temporary)
            self.assertEqual(result.returncode, 1)
            self.assertIn("bundle contains no Markdown records", result.stdout)


if __name__ == "__main__":
    unittest.main()
