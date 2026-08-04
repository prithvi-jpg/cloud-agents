#!/usr/bin/env python3
"""Validate the lean Agent Systems Foundry project spine with no dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


EXPECTED: dict[str, list[tuple[str, ...]]] = {
    "AGENTS.md": [
        ("## Source of truth",),
        ("## Scope and authority",),
        ("## Definition of done",),
    ],
    "docs/agent/PROJECT.md": [
        ("## Outcome and users",),
        ("## Baseline and causal problem", "## Baseline and problem"),
        ("## Constraints and non-goals",),
        ("## Quality bar and references",),
        ("## Authority and approval boundary",),
        ("## Canonical sources and evidence standard",),
        ("## Acceptance criteria and completion proof",),
    ],
    "docs/agent/STATE.md": [
        ("## Objective and phase",),
        ("## Verified evidence",),
        ("## Decisions and rejected paths",),
        ("## Assumptions, risks, and open questions",),
        ("## Authority boundary",),
        ("## Verification status",),
        ("## Handoff note",),
    ],
}


def validate(root: Path) -> dict[str, object]:
    files: list[dict[str, object]] = []
    errors: list[str] = []

    for relative, heading_groups in EXPECTED.items():
        target = root / relative
        item: dict[str, object] = {"path": str(target), "exists": target.is_file()}
        if not target.is_file():
            item["missing_headings"] = [" or ".join(group) for group in heading_groups]
            errors.append(f"Missing required file: {relative}")
            files.append(item)
            continue

        text = target.read_text(encoding="utf-8")
        missing = [
            " or ".join(group)
            for group in heading_groups
            if not any(heading in text for heading in group)
        ]
        item["missing_headings"] = missing
        item["bytes"] = len(text.encode("utf-8"))
        if missing:
            errors.append(f"{relative} is missing headings: {', '.join(missing)}")

        if relative.endswith("STATE.md"):
            next_action_match = re.search(
                r"^## Active plan(?: and)?(?: one)? next action\s*$([\s\S]*?)(?=^## |\Z)",
                text,
                flags=re.MULTILINE | re.IGNORECASE,
            )
            has_next_action = bool(
                next_action_match and next_action_match.group(1).strip()
            )
            item["has_next_action"] = has_next_action
            if not has_next_action:
                errors.append(
                    "docs/agent/STATE.md needs a non-empty active-plan/next-action section"
                )

        files.append(item)

    return {
        "ok": not errors,
        "root": str(root),
        "errors": errors,
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate AGENTS.md and docs/agent PROJECT/STATE structure."
    )
    parser.add_argument("--root", required=True, help="Project root to validate")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(
            json.dumps(
                {"ok": False, "root": str(root), "errors": ["Root is not a directory"]},
                indent=2,
            )
        )
        raise SystemExit(2)

    result = validate(root)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
