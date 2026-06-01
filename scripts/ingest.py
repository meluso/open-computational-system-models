#!/usr/bin/env python3
"""One-shot ingestion of researched entry blocks into data/entries/*.yml.

Reads raw block files (data/_raw/*.txt) where each entry is wrapped as:
    ----8<---- BEGIN <id> ----8<----
    <yaml>
    ----8<---- END <id> ----8<----

Sanitizes each entry against the schema's allowed keys (drops stray keys some
sources added), dedupes by id (first wins), and writes clean YAML. Anything
outside BEGIN/END markers (including the agents' trailing NOTES) is ignored.

Usage: python scripts/ingest.py [--dry-run]
"""
from __future__ import annotations

import datetime as _dt
import json
import pathlib
import re
import sys

import yaml


def stringify_dates(obj):
    """YAML auto-parses unquoted ISO dates into date objects; the schema wants
    strings. Convert any date/datetime back to an ISO string, recursively."""
    if isinstance(obj, (_dt.date, _dt.datetime)):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: stringify_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [stringify_dates(v) for v in obj]
    return obj

from common import ENTRIES_DIR, REPO_ROOT, SCHEMA_FILE

RAW_DIR = REPO_ROOT / "data" / "_raw"
BLOCK_RE = re.compile(
    r"----8<----\s*BEGIN\s+(?P<id>[a-z0-9-]+)\s*----8<----\n(?P<body>.*?)\n----8<----\s*END",
    re.DOTALL,
)


def allowed_keys() -> tuple[set, dict]:
    schema = json.loads(SCHEMA_FILE.read_text())
    top = set(schema["properties"].keys())
    nested = {}
    for k in ("scale", "maintenance_status", "verification_confidence"):
        nested[k] = set(schema["properties"][k]["properties"].keys())
    return top, nested


def sanitize(entry: dict, top: set, nested: dict) -> tuple[dict, list[str]]:
    dropped = []
    clean = {}
    for k, v in entry.items():
        if k not in top:
            dropped.append(k)
            continue
        if k in nested and isinstance(v, dict):
            subclean = {}
            for sk, sv in v.items():
                if sk in nested[k]:
                    subclean[sk] = sv
                else:
                    dropped.append(f"{k}.{sk}")
            clean[k] = subclean
        else:
            clean[k] = v
    return clean, dropped


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    top, nested = allowed_keys()
    ENTRIES_DIR.mkdir(parents=True, exist_ok=True)

    seen: dict[str, str] = {}
    written = 0
    for raw in sorted(RAW_DIR.glob("*.txt")):
        text = raw.read_text()
        for m in BLOCK_RE.finditer(text):
            marker_id = m.group("id")
            body = m.group("body")
            try:
                entry = yaml.safe_load(body)
            except yaml.YAMLError as e:
                print(f"  YAML ERROR in {raw.name} block {marker_id}: {e}")
                continue
            if not isinstance(entry, dict):
                print(f"  SKIP non-dict block {marker_id} in {raw.name}")
                continue
            entry = stringify_dates(entry)
            # Marker id is authoritative.
            entry["id"] = marker_id
            if marker_id in seen:
                print(f"  DEDUP: skipping duplicate '{marker_id}' from {raw.name} "
                      f"(kept from {seen[marker_id]})")
                continue
            seen[marker_id] = raw.name
            clean, dropped = sanitize(entry, top, nested)
            if dropped:
                print(f"  {marker_id}: dropped stray keys: {', '.join(dropped)}")
            if not dry:
                out = ENTRIES_DIR / f"{marker_id}.yml"
                with open(out, "w", encoding="utf-8") as fh:
                    yaml.safe_dump(
                        clean, fh, sort_keys=False, allow_unicode=True,
                        default_flow_style=False, width=100,
                    )
            written += 1

    print(f"\nIngested {written} unique entries"
          + (" (dry run, nothing written)" if dry else f" into {ENTRIES_DIR.relative_to(REPO_ROOT)}"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
