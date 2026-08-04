#!/usr/bin/env python3
"""Validate Foundry Markdown memory records without third-party dependencies."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys
from typing import Any


REQUIRED = {
    "id",
    "type",
    "scope",
    "status",
    "created_at",
    "updated_at",
    "source_refs",
    "confidence",
    "privacy",
    "tags",
    "related",
    "supersedes",
    "stale_after",
}
TYPES = {"preference", "decision", "fact", "lesson", "failure", "procedure", "checkpoint"}
STATUSES = {"active", "tentative", "superseded", "stale", "rejected"}
CONFIDENCE = {"observed", "confirmed", "inferred"}
PRIVACY = {"public", "internal", "sensitive"}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{2,127}$")


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"null", "~"}:
        return None
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("["):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError(f"lists must use JSON-compatible YAML: {exc}") from exc
        if not isinstance(parsed, list):
            raise ValueError("bracket value must be a list")
        return parsed
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_record(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML frontmatter delimiter")
    closing = text.find("\n---\n", 4)
    if closing < 0:
        raise ValueError("missing closing YAML frontmatter delimiter")
    raw = text[4:closing]
    body = text[closing + 5 :].strip()
    metadata: dict[str, Any] = {}
    for index, line in enumerate(raw.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            raise ValueError(f"line {index}: only flat key: value frontmatter is supported")
        key, value = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            raise ValueError(f"line {index}: duplicate key {key}")
        metadata[key] = parse_scalar(value)
    return metadata, body


def valid_datetime(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        datetime.fromisoformat(candidate)
    except ValueError:
        return False
    return True


def validate_metadata(metadata: dict[str, Any], body: str) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED - metadata.keys())
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if not ID_PATTERN.fullmatch(str(metadata.get("id", ""))):
        errors.append("id must match ^[a-z0-9][a-z0-9._-]{2,127}$")
    if metadata.get("type") not in TYPES:
        errors.append(f"invalid type: {metadata.get('type')}")
    if metadata.get("status") not in STATUSES:
        errors.append(f"invalid status: {metadata.get('status')}")
    if metadata.get("confidence") not in CONFIDENCE:
        errors.append(f"invalid confidence: {metadata.get('confidence')}")
    if metadata.get("privacy") not in PRIVACY:
        errors.append(f"invalid privacy: {metadata.get('privacy')}")
    if not isinstance(metadata.get("scope"), str) or not metadata.get("scope"):
        errors.append("scope must be a non-empty string")
    for key in ("created_at", "updated_at"):
        if not valid_datetime(metadata.get(key)):
            errors.append(f"{key} must be an ISO-8601 datetime")
    stale_after = metadata.get("stale_after")
    if stale_after is not None and not valid_datetime(stale_after):
        errors.append("stale_after must be null or an ISO-8601 datetime")
    for key in ("source_refs", "tags", "related", "supersedes"):
        value = metadata.get(key)
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            errors.append(f"{key} must be a JSON-compatible list of strings")
    if isinstance(metadata.get("source_refs"), list) and not metadata["source_refs"]:
        errors.append("source_refs must contain at least one source")
    if not body:
        errors.append("record body must not be empty")
    return errors


def validate(root: Path) -> dict[str, Any]:
    files = sorted(root.rglob("*.md"))
    results: list[dict[str, Any]] = []
    seen: dict[str, str] = {}
    all_errors: list[str] = []
    parsed_records: list[tuple[Path, dict[str, Any]]] = []

    for path in files:
        relative = str(path.relative_to(root))
        try:
            metadata, body = parse_record(path)
            errors = validate_metadata(metadata, body)
        except (OSError, UnicodeError, ValueError) as exc:
            metadata = {}
            errors = [str(exc)]
        record_id = metadata.get("id")
        if isinstance(record_id, str):
            if record_id in seen:
                errors.append(f"duplicate id also used by {seen[record_id]}")
            else:
                seen[record_id] = relative
            parsed_records.append((path, metadata))
        results.append({"path": relative, "id": record_id, "errors": errors})
        all_errors.extend(f"{relative}: {error}" for error in errors)

    warnings: list[str] = []
    known = set(seen)
    for path, metadata in parsed_records:
        for key in ("related", "supersedes"):
            for target in metadata.get(key, []) if isinstance(metadata.get(key), list) else []:
                if target not in known:
                    warnings.append(f"{path.relative_to(root)}: {key} references unknown id {target}")

    if not files:
        all_errors.append("bundle contains no Markdown records")
    return {
        "ok": not all_errors,
        "root": str(root),
        "records": len(files),
        "errors": all_errors,
        "warnings": warnings,
        "files": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Foundry Markdown memory bundle.")
    parser.add_argument("--root", required=True, help="Directory containing memory Markdown files")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(json.dumps({"ok": False, "root": str(root), "errors": ["root is not a directory"]}, indent=2))
        raise SystemExit(2)
    result = validate(root)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
