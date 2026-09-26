#!/usr/bin/env python3
"""Validate an HCI Agent Test Lab run and its authority receipts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lab_common import read_json

CLAIM_TYPES = {"observed", "interpreted", "specified", "simulated", "unknown"}
SEVERITIES = {"blocker", "high", "medium", "low", "note"}
STATUSES = {"completed", "blocked", "failed"}


def require_fields(value: dict[str, Any], fields: list[str], location: str, errors: list[str]) -> None:
    for field in fields:
        if field not in value:
            errors.append(f"{location}: missing {field}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--require-aggregate", action="store_true")
    args = parser.parse_args()
    run_dir = args.run_dir.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        errors.append("manifest.json is missing")
        manifest: dict[str, Any] = {}
    else:
        manifest = read_json(manifest_path)
        require_fields(
            manifest,
            ["schema_version", "run_id", "target", "mission", "authority", "cohort", "status"],
            "manifest",
            errors,
        )
        if manifest.get("schema_version") != "0.1":
            errors.append("manifest: unsupported schema_version")
        if manifest.get("authority", {}).get("mode") not in {"read-only", "sandbox-write"}:
            errors.append("manifest: invalid authority mode")

    for item in manifest.get("cohort", []):
        agent_id = str(item.get("agent_id", "missing-agent"))
        profile_path = run_dir / str(item.get("profile_path", ""))
        if not profile_path.exists():
            errors.append(f"{agent_id}: profile is missing")
        result_path = run_dir / "results" / f"{agent_id}.json"
        if not result_path.exists():
            message = f"{agent_id}: result is missing"
            (errors if args.require_complete else warnings).append(message)
            continue
        result = read_json(result_path)
        require_fields(
            result,
            [
                "schema_version",
                "run_id",
                "agent_id",
                "profile_id",
                "status",
                "browser",
                "task_outcome",
                "path",
                "findings",
                "positive_signals",
                "open_questions",
                "authority_receipt",
            ],
            agent_id,
            errors,
        )
        if result.get("run_id") != manifest.get("run_id"):
            errors.append(f"{agent_id}: run_id does not match manifest")
        if result.get("status") not in STATUSES:
            errors.append(f"{agent_id}: invalid status")
        receipt = result.get("authority_receipt", {})
        if manifest.get("authority", {}).get("mode") == "read-only":
            if receipt.get("external_writes") != 0 or receipt.get("target_writes") != 0:
                errors.append(f"{agent_id}: read-only authority receipt reports writes")
        for finding in result.get("findings", []):
            finding_id = str(finding.get("id", "missing-finding-id"))
            claim_type = finding.get("claim_type")
            if claim_type not in CLAIM_TYPES:
                errors.append(f"{agent_id}/{finding_id}: invalid claim_type")
            if finding.get("severity") not in SEVERITIES:
                errors.append(f"{agent_id}/{finding_id}: invalid severity")
            if claim_type in {"observed", "specified"} and not finding.get("evidence_refs"):
                errors.append(f"{agent_id}/{finding_id}: {claim_type} finding lacks evidence")
            if claim_type == "unknown" and finding.get("human_required") is not True:
                warnings.append(f"{agent_id}/{finding_id}: unknown finding should require human review")

    if args.require_aggregate:
        for name in ("aggregate.json", "FINDINGS.md", "HANDOFF.md", "test-room.html"):
            if not (run_dir / name).exists():
                errors.append(f"{name} is missing")

    receipt = {
        "run_dir": str(run_dir),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(receipt, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
