#!/usr/bin/env python3
"""Validate every catalog entry against schema/entry.schema.json and a set of
cross-entry rules. Fails loudly: any missing mandatory field, malformed entry,
or rule violation prints an error and exits non-zero.

Usage:
    python scripts/validate.py            # validate, exit 1 on any error
    python scripts/validate.py --quiet    # only print on error / summary line
"""
from __future__ import annotations

import json
import sys

import jsonschema

from common import (
    SCHEMA_FILE,
    UNSTATED,
    domain_slugs,
    is_unstated,
    load_entries,
    parse_iso_date,
)


def load_schema() -> dict:
    with open(SCHEMA_FILE, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv: list[str]) -> int:
    quiet = "--quiet" in argv
    schema = load_schema()
    validator = jsonschema.Draft7Validator(schema)
    valid_domains = set(domain_slugs())
    entries = load_entries()

    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: dict[str, str] = {}

    if not entries:
        errors.append("No entries found under data/entries/*.yml")

    for entry in entries:
        path = entry.get("_path", "<unknown>")
        # Strip private bookkeeping keys before schema validation.
        stem = entry.get("_stem")
        clean = {k: v for k, v in entry.items() if not k.startswith("_")}

        # 1. JSON Schema validation (mandatory fields, types, enums).
        schema_errors = sorted(
            validator.iter_errors(clean), key=lambda e: list(e.absolute_path)
        )
        for err in schema_errors:
            loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
            errors.append(f"{path}: schema error at '{loc}': {err.message}")

        entry_id = clean.get("id")

        # 2. id must match filename stem.
        if entry_id and stem and entry_id != stem:
            errors.append(
                f"{path}: id '{entry_id}' does not match filename stem '{stem}'"
            )

        # 3. id must be unique.
        if entry_id:
            if entry_id in seen_ids:
                errors.append(
                    f"{path}: duplicate id '{entry_id}' (also in {seen_ids[entry_id]})"
                )
            else:
                seen_ids[entry_id] = path

        # 4. domain must be registered (schema enum already covers this, but
        #    keep an explicit message in case the enum and registry drift).
        domain = clean.get("domain")
        if domain and domain not in valid_domains:
            errors.append(
                f"{path}: domain '{domain}' is not in data/domains.yml registry"
            )

        # 5. last_verified must be a real ISO date.
        lv = clean.get("last_verified")
        if lv is not None and parse_iso_date(lv) is None:
            errors.append(f"{path}: last_verified '{lv}' is not a valid ISO date")

        # 6. verification_confidence.unverified should name fields that are
        #    actually unstated, and any unstated volatile field should be listed.
        vc = clean.get("verification_confidence", {}) or {}
        declared_unverified = set(vc.get("unverified", []) or [])
        # Accept either dotted names ("maintenance_status.latest_version") or the
        # bare leaf ("latest_version") in the unverified list.
        declared_leaves = {d.split(".")[-1] for d in declared_unverified}
        # Detect unstated sentinels in common volatile fields.
        unstated_fields = set()
        if is_unstated(clean.get("license")):
            unstated_fields.add("license")
        scale = clean.get("scale", {}) or {}
        if is_unstated(scale.get("element_count")):
            unstated_fields.add("scale.element_count")
        ms = clean.get("maintenance_status", {}) or {}
        if is_unstated(ms.get("latest_version")):
            unstated_fields.add("maintenance_status.latest_version")
        if is_unstated(ms.get("latest_release_date")):
            unstated_fields.add("maintenance_status.latest_release_date")
        for f in unstated_fields:
            if f not in declared_unverified and f.split(".")[-1] not in declared_leaves:
                warnings.append(
                    f"{path}: field '{f}' is unstated but not listed in "
                    f"verification_confidence.unverified"
                )

        # 7. Soft inclusion-test check: warn if a representative element count is
        #    a plain number at or below 25 (the threshold), since the model may
        #    fail the >25-element inclusion test.
        ec = scale.get("element_count")
        if isinstance(ec, str) and not is_unstated(ec):
            digits = "".join(ch for ch in ec if ch.isdigit())
            # Only when the string is essentially just a small number.
            if digits and ec.strip().rstrip("+").isdigit():
                if int(digits) <= 25:
                    warnings.append(
                        f"{path}: element_count '{ec}' is <= 25; confirm it meets "
                        f"the >25-element inclusion test"
                    )

        # 8. source_per_field should at least mention access_link / version /
        #    license provenance.
        spf = clean.get("source_per_field", {}) or {}
        if isinstance(spf, dict) and len(spf) == 0:
            errors.append(f"{path}: source_per_field must not be empty")

    # Report.
    n = len(entries)
    if errors:
        print(f"VALIDATION FAILED: {len(errors)} error(s) across {n} entrie(s).\n")
        for e in errors:
            print(f"  ERROR  {e}")
        if warnings and not quiet:
            print()
            for w in warnings:
                print(f"  warn   {w}")
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    if not quiet:
        if warnings:
            for w in warnings:
                print(f"  warn   {w}")
            print()
        # Per-domain counts for a quick sanity read.
        from collections import Counter

        counts = Counter(e.get("domain") for e in entries)
        print(f"VALIDATION PASSED: {n} entries, 0 errors, {len(warnings)} warning(s).")
        for slug in domain_slugs():
            if counts.get(slug):
                print(f"  {counts[slug]:>3}  {slug}")
    else:
        print(f"VALIDATION PASSED: {n} entries, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
