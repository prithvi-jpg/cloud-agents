#!/usr/bin/env python3
"""Run a dependency-free smoke test of the HCI Agent Test Lab scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from lab_common import read_json, utc_now, write_json


def run(*args: str) -> str:
    completed = subprocess.run(args, check=True, capture_output=True, text=True)
    return completed.stdout.strip()


def main() -> int:
    scripts = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="hci-agent-test-lab-") as temp:
        root = Path(temp)
        run_dir = Path(
            run(
                sys.executable,
                str(scripts / "init_run.py"),
                "--run-root",
                str(root / "runs"),
                "--target-name",
                "Fixture Product",
                "--workspace",
                str(root),
                "--url",
                "http://127.0.0.1:9999",
                "--mission",
                "Find and understand the safest next action.",
                "--profiles",
                "first-visit-navigator,evidence-skeptic,keyboard-pathfinder",
                "--run-id",
                "self-test",
            )
        )
        manifest = read_json(run_dir / "manifest.json")
        for index, item in enumerate(manifest["cohort"], start=1):
            agent_id = item["agent_id"]
            finding = {
                "id": f"{agent_id}-f1",
                "claim_type": "observed",
                "severity": "high" if index < 3 else "medium",
                "category": "orientation",
                "title": "Primary action lacks consequence detail",
                "observation": "The visible action label does not name the object or consequence.",
                "impact": "A tester cannot predict the next state before acting.",
                "evidence_refs": [f"snapshot:{agent_id}/initial.txt"],
                "confidence": "high",
                "human_required": False,
                "suggested_contract": "The primary action names its object and immediate consequence.",
            }
            result = {
                "schema_version": "0.1",
                "run_id": manifest["run_id"],
                "agent_id": agent_id,
                "profile_id": item["profile_id"],
                "status": "completed",
                "started_at": utc_now(),
                "completed_at": utc_now(),
                "browser": {
                    "adapter": "fixture",
                    "session": f"self-test-{agent_id}",
                    "viewport": "1440x1000",
                    "start_url": manifest["target"]["url"],
                    "final_url": manifest["target"]["url"],
                },
                "task_outcome": {
                    "state": "partial",
                    "summary": "The next action was visible but its consequence was unclear.",
                    "actions_used": index + 2,
                    "time_seconds": 20 + index,
                },
                "path": [
                    {
                        "step": 1,
                        "action": "opened fixture",
                        "observation": "Primary action visible",
                        "evidence_refs": [f"snapshot:{agent_id}/initial.txt"],
                    }
                ],
                "findings": [finding],
                "positive_signals": ["The mission area is visible on first render."],
                "open_questions": ["Would target users understand the product-specific terminology?"],
                "authority_receipt": {
                    "mode": "read-only",
                    "external_writes": 0,
                    "target_writes": 0,
                    "stopped_before": [],
                    "notes": "fixture only",
                },
            }
            write_json(run_dir / "results" / f"{agent_id}.json", result)
        run(sys.executable, str(scripts / "aggregate_run.py"), "--run-dir", str(run_dir))
        run(sys.executable, str(scripts / "render_test_room.py"), "--run-dir", str(run_dir))
        validation = json.loads(
            run(
                sys.executable,
                str(scripts / "validate_run.py"),
                "--run-dir",
                str(run_dir),
                "--require-complete",
                "--require-aggregate",
            )
        )
        aggregate = read_json(run_dir / "aggregate.json")
        html_text = (run_dir / "test-room.html").read_text(encoding="utf-8")
        assert validation["valid"]
        assert aggregate["status"] == "complete"
        assert aggregate["issues"][0]["agreement"] == 1.0
        assert "Living test room" in html_text
        print(json.dumps({"valid": True, "issues": len(aggregate["issues"]), "agents": 3}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
