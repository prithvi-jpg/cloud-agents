#!/usr/bin/env python3
"""Verify exact publicly cited emails without paid APIs or third-party packages."""

import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

EMAIL_RE = re.compile(r"^[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9-]+(?:\.[A-Z0-9-]+)+$", re.I)
OFFICIAL_TYPES = {
    "official_company",
    "official_personal",
    "official_university",
    "official_lab",
    "official_publication",
}


def fetch_source(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 outreach-source-check/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read(2_000_000).decode("utf-8", errors="ignore")


def mx_records(domain, timeout):
    endpoint = "https://dns.google/resolve?" + urllib.parse.urlencode({"name": domain, "type": "MX"})
    req = urllib.request.Request(endpoint, headers={"Accept": "application/dns-json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        payload = json.load(response)
    return [item.get("data", "") for item in payload.get("Answer", []) if item.get("type") == 15]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Lead queue CSV")
    parser.add_argument("--output", required=True, help="Verified queue CSV")
    parser.add_argument("--timeout", type=int, default=12)
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()

    with open(args.input, encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0]) if rows else []
    extra = [
        "email_source_type",
        "source_page_match",
        "mx_valid",
        "mx_records",
        "verification_provider",
        "verified_at",
        "email_status",
        "verification_notes",
    ]
    fields += [field for field in extra if field not in fields]

    counts = {"public_mx_valid": 0, "public_unconfirmed": 0, "invalid": 0, "not_found": 0}
    verified_at = datetime.now(timezone.utc).isoformat()
    for row in rows:
        email = row.get("email", "").strip().lower()
        source_url = row.get("email_source_url", "").strip()
        source_type = row.get("email_source_type", "").strip().lower()
        row.update(source_page_match="false", mx_valid="false", mx_records="", verification_provider="public-page+dns.google", verified_at=verified_at, verification_notes="")
        if not email:
            status = "not_found"
            row["verification_notes"] = "No exact public email supplied."
        elif not EMAIL_RE.fullmatch(email):
            status = "invalid"
            row["verification_notes"] = "Invalid email syntax."
        elif source_type not in OFFICIAL_TYPES or not source_url.startswith(("https://", "http://")):
            status = "public_unconfirmed"
            row["verification_notes"] = "Missing an approved official source type or URL."
        else:
            source_match = False
            records = []
            errors = []
            try:
                source_match = email in fetch_source(source_url, args.timeout).lower()
            except Exception as exc:
                errors.append(f"source fetch failed: {type(exc).__name__}")
            try:
                records = mx_records(email.rsplit("@", 1)[1], args.timeout)
            except Exception as exc:
                errors.append(f"MX lookup failed: {type(exc).__name__}")
            row["source_page_match"] = str(source_match).lower()
            row["mx_valid"] = str(bool(records)).lower()
            row["mx_records"] = " | ".join(records)
            status = "public_mx_valid" if source_match and records else "public_unconfirmed"
            row["verification_notes"] = "; ".join(errors)
        row["email_status"] = status
        counts[status] += 1
        time.sleep(args.delay)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"rows": len(rows), "counts": counts, "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
