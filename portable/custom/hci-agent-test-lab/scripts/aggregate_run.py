#!/usr/bin/env python3
"""Aggregate tester results into evidence and product-agent handoff artifacts."""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from lab_common import read_json, severity_rank, utc_now, write_json


def normalized_key(finding: dict[str, Any]) -> str:
    title = re.sub(r"[^a-z0-9]+", " ", str(finding.get("title", "")).lower()).strip()
    category = str(finding.get("category", "uncategorized")).lower().strip()
    contract = re.sub(
        r"[^a-z0-9]+",
        " ",
        str(finding.get("suggested_contract") or "").lower(),
    ).strip()
    return f"{category}|{contract or title}"


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    args = parser.parse_args()
    run_dir = args.run_dir.expanduser().resolve()
    manifest = read_json(run_dir / "manifest.json")
    profiles = {
        item["agent_id"]: read_json(run_dir / item["profile_path"])
        for item in manifest.get("cohort", [])
    }

    results: list[dict[str, Any]] = []
    missing: list[str] = []
    for agent_id in profiles:
        path = run_dir / "results" / f"{agent_id}.json"
        if path.exists():
            results.append(read_json(path))
        else:
            missing.append(agent_id)

    grouped: dict[str, list[tuple[dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    positive_signals: list[dict[str, str]] = []
    unknowns: list[dict[str, str]] = []
    for result in results:
        for finding in result.get("findings", []):
            grouped[normalized_key(finding)].append((result, finding))
        for signal in result.get("positive_signals", []):
            positive_signals.append({"agent_id": result["agent_id"], "signal": str(signal)})
        for question in result.get("open_questions", []):
            unknowns.append({"agent_id": result["agent_id"], "question": str(question)})

    issues: list[dict[str, Any]] = []
    for index, group in enumerate(grouped.values(), start=1):
        agents = sorted({result["agent_id"] for result, _ in group})
        representative = max(group, key=lambda item: severity_rank(str(item[1].get("severity", "note"))))[1]
        evidence_refs = sorted(
            {
                str(ref)
                for _, finding in group
                for ref in finding.get("evidence_refs", [])
                if str(ref).strip()
            }
        )
        issues.append(
            {
                "id": f"I-{index:03d}",
                "title": representative.get("title", "Untitled finding"),
                "category": representative.get("category", "uncategorized"),
                "severity": representative.get("severity", "note"),
                "claim_types": sorted({str(finding.get("claim_type", "unknown")) for _, finding in group}),
                "agent_ids": agents,
                "profile_ids": sorted({str(result.get("profile_id", "")) for result, _ in group}),
                "agreement": round(len(agents) / max(1, len(profiles)), 2),
                "observation": representative.get("observation", ""),
                "impact": representative.get("impact", ""),
                "evidence_refs": evidence_refs,
                "human_required": any(bool(finding.get("human_required")) for _, finding in group),
                "suggested_contract": representative.get("suggested_contract"),
            }
        )
    issues.sort(key=lambda issue: (-severity_rank(str(issue["severity"])), -float(issue["agreement"])))
    for index, issue in enumerate(issues, start=1):
        issue["id"] = f"I-{index:03d}"

    status = "complete" if results and not missing else ("partial" if results else "blocked")
    aggregate = {
        "schema_version": manifest.get("schema_version", "0.1"),
        "run_id": manifest["run_id"],
        "generated_at": utc_now(),
        "status": status,
        "tester_count": len(profiles),
        "completed_result_count": len(results),
        "missing_agents": missing,
        "issues": issues,
        "positive_signals": positive_signals,
        "unknowns": unknowns,
        "disagreement_notes": [
            f"{issue['id']} was reported by {len(issue['agent_ids'])}/{len(profiles)} profiles."
            for issue in issues
            if len(issue["agent_ids"]) < len(profiles)
        ],
    }
    write_json(run_dir / "aggregate.json", aggregate)

    findings_lines = [
        f"# Findings: {manifest['target']['name']}",
        "",
        f"Mission: {manifest['mission']}",
        "",
        f"Status: **{status}** · Results: {len(results)}/{len(profiles)} · Authority: **{manifest['authority']['mode']}**",
        "",
        "> These are simulated browser rehearsals. They are not participant research or population claims.",
        "",
        "## Prioritized findings",
        "",
        "| ID | Severity | Finding | Profiles | Evidence | Human needed |",
        "|---|---|---|---:|---:|---:|",
    ]
    if not issues:
        findings_lines.append("| — | — | No findings were recorded | 0 | 0 | yes |")
    for issue in issues:
        findings_lines.append(
            f"| {issue['id']} | {md_escape(issue['severity'])} | {md_escape(issue['title'])} | "
            f"{len(issue['agent_ids'])}/{len(profiles)} | {len(issue['evidence_refs'])} | "
            f"{'yes' if issue['human_required'] else 'no'} |"
        )
        findings_lines.extend(
            [
                "",
                f"### {issue['id']} — {issue['title']}",
                "",
                f"- Observation: {issue['observation'] or 'Not supplied'}",
                f"- Impact: {issue['impact'] or 'Not supplied'}",
                f"- Claim types: {', '.join(issue['claim_types'])}",
                f"- Profiles: {', '.join(issue['profile_ids'])}",
                f"- Evidence: {', '.join(issue['evidence_refs']) or 'missing'}",
                f"- Candidate contract: {issue['suggested_contract'] or 'none'}",
                "",
            ]
        )
    findings_lines.extend(["## Positive signals", ""])
    findings_lines.extend(
        [f"- `{item['agent_id']}`: {item['signal']}" for item in positive_signals]
        or ["- None recorded."]
    )
    findings_lines.extend(["", "## Unknowns and human-research boundary", ""])
    findings_lines.extend(
        [f"- `{item['agent_id']}`: {item['question']}" for item in unknowns]
        or ["- No open question was recorded; reviewer should verify that this is credible."]
    )
    if missing:
        findings_lines.extend(["", "## Missing results", "", f"- {', '.join(missing)}"])
    (run_dir / "FINDINGS.md").write_text("\n".join(findings_lines) + "\n", encoding="utf-8")

    handoff_lines = [
        f"# UX test handoff: {manifest['target']['name']}",
        "",
        "## Product-agent objective",
        "",
        f"Inspect the evidence below and improve the product only after the human owner accepts the findings. Preserve the target workspace’s own AGENTS.md, authority rules, and user edits.",
        "",
        "## Tested mission",
        "",
        manifest["mission"],
        "",
        "## Proposed work",
        "",
    ]
    actionable = [issue for issue in issues if issue["severity"] in {"blocker", "high", "medium"}]
    handoff_lines.extend(
        [
            f"{index}. **{issue['title']}** — {issue['impact'] or issue['observation']} "
            f"(evidence: {', '.join(issue['evidence_refs']) or 'missing; do not implement yet'})"
            for index, issue in enumerate(actionable, start=1)
        ]
        or ["1. No implementation-ready issue survived aggregation."]
    )
    handoff_lines.extend(
        [
            "",
            "## Acceptance boundary",
            "",
            "- Reproduce the issue in the target workspace before editing.",
            "- Do not implement findings without evidence.",
            "- Keep simulated reactions distinct from deterministic failures.",
            "- Preserve `unknown` questions for a person or qualified reviewer.",
            "- Rerun the same mission and profiles after any accepted fix.",
            "",
            "## Evidence",
            "",
            f"- Run: `{run_dir}`",
            "- Prioritized report: `FINDINGS.md`",
            "- Machine result: `aggregate.json`",
            "- Observer surface: `test-room.html`",
        ]
    )
    (run_dir / "HANDOFF.md").write_text("\n".join(handoff_lines) + "\n", encoding="utf-8")

    manifest["status"] = status
    manifest["aggregated_at"] = aggregate["generated_at"]
    write_json(run_dir / "manifest.json", manifest)
    print(run_dir / "aggregate.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
