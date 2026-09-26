#!/usr/bin/env python3
"""Initialize a bounded HCI Agent Test Lab run."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from lab_common import SCHEMA_VERSION, selected_profiles, slugify, utc_now, write_json

FORBIDDEN = [
    "external messages or publication",
    "purchases or billing changes",
    "permission or credential changes",
    "destructive actions",
    "production-data mutation",
    "automatic edits to the target workspace",
]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--target-name", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--mission", required=True)
    parser.add_argument(
        "--profiles",
        default="first-visit-navigator,evidence-skeptic,keyboard-pathfinder",
    )
    parser.add_argument("--mode", choices=("read-only", "sandbox-write"), default="read-only")
    parser.add_argument("--browser-adapter", default="auto")
    parser.add_argument("--build-id", default="unrecorded")
    parser.add_argument("--run-id")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    workspace = args.workspace.expanduser().resolve()
    if not workspace.exists():
        raise SystemExit(f"Workspace does not exist: {workspace}")
    if len(args.mission.strip()) < 8:
        raise SystemExit("Mission must describe one observable user job")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = args.run_id or f"{timestamp}-{slugify(args.target_name)[:32]}"
    run_dir = args.run_root.expanduser().resolve() / run_id
    if run_dir.exists():
        raise SystemExit(f"Run already exists: {run_dir}")

    profiles = selected_profiles(args.profiles)
    for relative in ("profiles", "results", "traces", "screenshots"):
        (run_dir / relative).mkdir(parents=True, exist_ok=False)

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "created_at": utc_now(),
        "target": {
            "name": args.target_name.strip(),
            "workspace": str(workspace),
            "url": args.url.strip(),
            "build_id": args.build_id.strip(),
        },
        "mission": args.mission.strip(),
        "authority": {
            "mode": args.mode,
            "allowed": (
                ["read browser-visible local state and create run artifacts"]
                if args.mode == "read-only"
                else ["mutate only the declared resettable synthetic fixture and create run artifacts"]
            ),
            "forbidden": FORBIDDEN,
        },
        "browser": {
            "adapter": args.browser_adapter,
            "session_pattern": f"{run_id}-<agent-id>",
            "required_evidence": ["initial snapshot", "decisive trace", "authority receipt"],
        },
        "cohort": [
            {
                "agent_id": profile["agent_id"],
                "profile_id": profile["id"],
                "profile_path": f"profiles/{profile['agent_id']}.json",
            }
            for profile in profiles
        ],
        "claim_boundary": {
            "allowed": ["observed", "interpreted", "specified", "simulated", "unknown"],
            "never_infer": [
                "population prevalence",
                "real user emotion or preference",
                "adoption or market demand",
                "lived accessibility experience",
            ],
        },
        "status": "initialized",
    }
    write_json(run_dir / "manifest.json", manifest)
    for profile in profiles:
        write_json(run_dir / "profiles" / f"{profile['agent_id']}.json", profile)

    run_note = (
        f"# Run {run_id}\n\n"
        f"- Target: {manifest['target']['name']}\n"
        f"- URL: {manifest['target']['url']}\n"
        f"- Mission: {manifest['mission']}\n"
        f"- Authority: {manifest['authority']['mode']}\n"
        f"- Cohort: {', '.join(item['profile_id'] for item in manifest['cohort'])}\n\n"
        "The profiles are simulated test configurations. Their paths are not human research.\n"
    )
    (run_dir / "RUN.md").write_text(run_note, encoding="utf-8")
    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
