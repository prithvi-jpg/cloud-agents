#!/usr/bin/env python3
"""Initialize the lean Agent Systems Foundry project spine without overwriting files."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys


def fail(message: str) -> None:
    print(json.dumps({"ok": False, "error": message}, indent=2))
    raise SystemExit(2)


def validate_root(raw_root: str) -> Path:
    root = Path(raw_root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        fail(f"Project root must already exist and be a directory: {root}")
    if root == Path(root.anchor) or root == Path.home().resolve():
        fail(f"Refusing to initialize a broad root directory: {root}")
    return root


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.foundry-tmp-{os.getpid()}")
    temporary.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")
    os.replace(temporary, path)


def build_files(name: str, outcome: str, authority: str) -> dict[str, str]:
    agents = f"""# {name}

## Source of truth

- Direct user instructions and edits in this project take priority.
- Canonical project framing lives in `docs/agent/PROJECT.md`.
- Current working truth lives in `docs/agent/STATE.md`.
- Preserve source evidence before interpretation.

## Scope and authority

- {authority}
- Preview and obtain explicit approval before external, public, costly, destructive, credentialed, irreversible, or durable self-modifying actions.

## Stable conventions

- Read the project contract and state before meaningful work.
- Use the smallest competent capability set.
- Keep user requirements, facts, inferences, assumptions, and proposals distinct.
- Verify the actual artifact before claiming completion.

## Definition of done

- The requested artifact exists and satisfies the project acceptance criteria.
- Claims link to fresh evidence.
- Known limitations and one next action are recorded.
"""

    project = f"""# Project

## Outcome and users

{outcome}

## Baseline and causal problem

TBD collaboratively from project evidence.

## Constraints and non-goals

- TBD

## Quality bar and references

- TBD

## Authority and approval boundary

- {authority}
- Explicit approval is required before consequential external or durable actions.

## Canonical sources and evidence standard

- Direct user instructions and edits are primary.
- Add project-specific sources with provenance and freshness.

## Human steering points

- Preview taste-sensitive or direction-locking choices early enough to redirect.

## Acceptance criteria and completion proof

- TBD with artifact-specific verification.
"""

    state = f"""# State

## Objective and phase

Objective: {outcome}

Current phase: orient.

## Active plan and one next action

Next best action: inspect the existing project and collaboratively resolve any missing outcome, quality, authority, or completion criteria.

## Verified evidence

- Project spine initialized; no implementation claim has been made.

## Decisions and rejected paths

- None yet.

## Assumptions, risks, and open questions

- Project-specific framing remains to be completed.

## Capability shortlist and rationale

- Not selected; route capabilities after the current phase and uncertainty are clear.

## Authority boundary

- {authority}
- Consequential external or durable actions require explicit approval.

## Verification status

The project spine exists. Project-specific acceptance criteria and implementation remain unverified.

## Handoff note

Read `AGENTS.md`, `docs/agent/PROJECT.md`, and this state. Treat later user edits as authoritative.
"""

    return {
        "AGENTS.md": agents,
        "docs/agent/PROJECT.md": project,
        "docs/agent/STATE.md": state,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create AGENTS.md, docs/agent/PROJECT.md, and docs/agent/STATE.md without overwriting existing files."
    )
    parser.add_argument("--root", required=True, help="Existing project root")
    parser.add_argument("--name", required=True, help="Human-readable project name")
    parser.add_argument(
        "--outcome",
        default="TBD collaboratively with the user.",
        help="Initial outcome statement",
    )
    parser.add_argument(
        "--authority",
        default="Proceed with scoped, reversible local work after alignment.",
        help="Default local authority statement",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report intended actions without writing",
    )
    args = parser.parse_args()

    root = validate_root(args.root)
    files = build_files(args.name.strip(), args.outcome.strip(), args.authority.strip())
    receipt: list[dict[str, str]] = []

    for relative, content in files.items():
        target = root / relative
        if target.exists():
            receipt.append({"path": str(target), "status": "skipped_existing"})
            continue
        if args.dry_run:
            receipt.append({"path": str(target), "status": "would_create"})
            continue
        atomic_write(target, content)
        receipt.append({"path": str(target), "status": "created"})

    print(
        json.dumps(
            {
                "ok": True,
                "root": str(root),
                "dry_run": args.dry_run,
                "files": receipt,
                "next_action": "Review and complete PROJECT.md before material implementation.",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
