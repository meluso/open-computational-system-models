"""Shared loaders for the catalog tooling.

One place that knows where data lives and how to read it, so validate.py and
build.py never drift apart.
"""
from __future__ import annotations

import datetime as _dt
import pathlib
import re

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
ENTRIES_DIR = DATA_DIR / "entries"
DOMAINS_FILE = DATA_DIR / "domains.yml"
SCHEMA_FILE = REPO_ROOT / "schema" / "entry.schema.json"

# Sentinel allowed in volatile fields per the brief: better an explicit
# "unstated" than a confident guess.
UNSTATED = "unstated — needs direct verification"


def load_yaml(path: pathlib.Path):
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_domains() -> list[dict]:
    """Return the ordered list of domain dicts from data/domains.yml."""
    data = load_yaml(DOMAINS_FILE)
    return data["domains"]


def domain_slugs() -> list[str]:
    return [d["slug"] for d in load_domains()]


def entry_paths() -> list[pathlib.Path]:
    if not ENTRIES_DIR.exists():
        return []
    return sorted(ENTRIES_DIR.glob("*.yml"))


def load_entries() -> list[dict]:
    """Load every entry, attaching its source path under the private key _path."""
    entries = []
    for path in entry_paths():
        entry = load_yaml(path)
        if entry is None:
            continue
        entry["_path"] = str(path.relative_to(REPO_ROOT))
        entry["_stem"] = path.stem
        entries.append(entry)
    return entries


def is_unstated(value) -> bool:
    return isinstance(value, str) and value.strip() == UNSTATED


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_iso_date(value: str):
    if not isinstance(value, str) or not _DATE_RE.match(value):
        return None
    try:
        return _dt.date.fromisoformat(value)
    except ValueError:
        return None
