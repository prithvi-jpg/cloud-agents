#!/usr/bin/env python3
"""Shared helpers for the HCI Agent Test Lab."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "0.1"

DEFAULT_PROFILES: dict[str, dict[str, Any]] = {
    "first-visit-navigator": {
        "name": "Mira",
        "lens": "Infer the product model and first useful action without prior product history.",
        "starting_knowledge": ["Only the mission and visible interface copy."],
        "behavioral_constraints": [
            "Do not inspect source code before the first browser pass.",
            "Follow the strongest visible information scent.",
            "Record the first point where the product model becomes clear or ambiguous.",
        ],
        "mission_questions": [
            "Can a newcomer explain where they are and what to do next?",
            "Does the first action match the stated mission?",
        ],
        "time_budget_seconds": 240,
        "max_actions": 20,
        "stop_conditions": ["Stop before any consequential or external action."],
        "claim_boundary": "Cannot establish population comprehension, preference, or adoption.",
        "character": {"color": "#E96932", "accent": "#FFD45A", "station": "orientation"},
    },
    "timeboxed-operator": {
        "name": "Pax",
        "lens": "Find one safe next action within a ninety-second attention budget.",
        "starting_knowledge": ["The mission and the product name."],
        "behavioral_constraints": [
            "Spend no more than ninety seconds before choosing or declaring no clear action.",
            "Prefer the most prominent safe action.",
            "Record text or navigation that competes with the primary job.",
        ],
        "mission_questions": [
            "Is the next worthwhile action visible without exhaustive reading?",
            "Does priority match consequence?",
        ],
        "time_budget_seconds": 90,
        "max_actions": 12,
        "stop_conditions": ["Stop when the attention budget expires or an unsafe action is next."],
        "claim_boundary": "Cannot establish that real users share this attention budget.",
        "character": {"color": "#3167C6", "accent": "#BBD5FF", "station": "flow"},
    },
    "evidence-skeptic": {
        "name": "Sol",
        "lens": "Audit provenance, freshness, uncertainty, and fact-versus-interpretation boundaries.",
        "starting_knowledge": ["The mission and any declared evidence contract."],
        "behavioral_constraints": [
            "Open evidence details before accepting an AI recommendation.",
            "Look for freshness, source, confidence, and correction paths.",
            "Do not treat polished copy as proof.",
        ],
        "mission_questions": [
            "Why should a user trust the recommendation?",
            "Can an assertion be traced and corrected?",
        ],
        "time_budget_seconds": 300,
        "max_actions": 24,
        "stop_conditions": ["Stop when evidence is unavailable or leaves the declared target."],
        "claim_boundary": "Cannot establish real-world truth beyond the visible source records.",
        "character": {"color": "#6B4BC3", "accent": "#DCCBFF", "station": "evidence"},
    },
    "keyboard-pathfinder": {
        "name": "Kite",
        "lens": "Complete the mission with keyboard-only input and inspect semantic focus behavior.",
        "starting_knowledge": ["The mission and standard keyboard interaction conventions."],
        "behavioral_constraints": [
            "Use Tab, Shift+Tab, Enter, Space, and Escape instead of pointer input.",
            "Record focus order, visible focus, accessible names, traps, and recovery.",
            "Do not claim lived accessibility experience.",
        ],
        "mission_questions": [
            "Are the critical controls reachable and understandable by keyboard?",
            "Can the user escape, undo, or recover?",
        ],
        "time_budget_seconds": 300,
        "max_actions": 30,
        "stop_conditions": ["Stop at a focus trap, authority boundary, or completed mission."],
        "claim_boundary": "Mechanical keyboard evidence does not prove accessibility conformance.",
        "character": {"color": "#147D64", "accent": "#A9E8D7", "station": "flow"},
    },
    "recovery-explorer": {
        "name": "Rue",
        "lens": "Take one reversible wrong turn and determine whether the product supports repair.",
        "starting_knowledge": ["The mission and a resettable synthetic fixture."],
        "behavioral_constraints": [
            "Choose one plausible but reversible wrong path.",
            "Attempt to cancel, go back, undo, or correct without losing safe input.",
            "Do not seed irreversible errors.",
        ],
        "mission_questions": [
            "Does the interface explain what happened?",
            "Can the user recover without restarting or guessing?",
        ],
        "time_budget_seconds": 300,
        "max_actions": 24,
        "stop_conditions": ["Stop before irreversible state or when recovery succeeds or fails."],
        "claim_boundary": "Cannot estimate how often real users make this error.",
        "character": {"color": "#B5405B", "accent": "#FFC1CF", "station": "recovery"},
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "run"


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def selected_profiles(profile_csv: str) -> list[dict[str, Any]]:
    profile_ids = [item.strip() for item in profile_csv.split(",") if item.strip()]
    if not profile_ids:
        raise ValueError("Select at least one profile")
    unknown = [item for item in profile_ids if item not in DEFAULT_PROFILES]
    if unknown:
        supported = ", ".join(DEFAULT_PROFILES)
        raise ValueError(f"Unknown profiles: {', '.join(unknown)}. Supported: {supported}")
    output: list[dict[str, Any]] = []
    for index, profile_id in enumerate(profile_ids, start=1):
        profile = json.loads(json.dumps(DEFAULT_PROFILES[profile_id]))
        profile["id"] = profile_id
        profile["agent_id"] = f"agent-{index:02d}"
        output.append(profile)
    return output


def severity_rank(value: str) -> int:
    return {"note": 0, "low": 1, "medium": 2, "high": 3, "blocker": 4}.get(value, 0)
