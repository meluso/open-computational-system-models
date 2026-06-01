#!/usr/bin/env python3
"""Generate GAPS.md: every fact the catalog could not verify, so the maintainer
can do targeted manual checks. Derived directly from the entry data (and the
link-check JSON if present), so it stays accurate.

Usage:
    python scripts/check_links.py --json linkcheck.json   # optional, first
    python scripts/gaps.py                                 # writes GAPS.md
"""
from __future__ import annotations

import json
import pathlib

from common import REPO_ROOT, is_unstated, load_entries

LINKCHECK = REPO_ROOT / "linkcheck.json"
OUT = REPO_ROOT / "GAPS.md"

VOLATILE = [
    ("license", lambda e: e.get("license")),
    ("scale.element_count", lambda e: (e.get("scale") or {}).get("element_count")),
    ("maintenance_status.latest_version", lambda e: (e.get("maintenance_status") or {}).get("latest_version")),
    ("maintenance_status.latest_release_date", lambda e: (e.get("maintenance_status") or {}).get("latest_release_date")),
]


def main() -> int:
    entries = sorted(load_entries(), key=lambda e: (e["domain"], e["id"]))
    lines = []
    lines.append("# Gaps — Facts to Verify Manually\n")
    lines.append(
        "This file lists every volatile fact the catalog could not ground in a "
        "source, plus every entry whose overall verification confidence is below "
        "`high`. It is generated from the entry data by `scripts/gaps.py`. Use it "
        "for targeted manual checks. Nothing here was guessed: a fact is either "
        "marked with the sentinel `unstated — needs direct verification` or flagged "
        "in an entry's `verification_confidence`.\n"
    )

    # Summary counts.
    n = len(entries)
    by_conf = {"high": 0, "medium": 0, "low": 0}
    sentinel_count = 0
    for e in entries:
        by_conf[e.get("verification_confidence", {}).get("overall", "low")] = (
            by_conf.get(e.get("verification_confidence", {}).get("overall", "low"), 0) + 1
        )
        for _, getter in VOLATILE:
            if is_unstated(getter(e)):
                sentinel_count += 1
    lines.append("## Summary\n")
    lines.append(f"- Total entries: **{n}**")
    lines.append(
        f"- Overall confidence: **{by_conf.get('high',0)} high**, "
        f"**{by_conf.get('medium',0)} medium**, **{by_conf.get('low',0)} low**"
    )
    lines.append(f"- Fields carrying the explicit `unstated` sentinel: **{sentinel_count}**\n")

    # Per-entry gaps.
    lines.append("## Per-entry unverified facts\n")
    lines.append(
        "Only entries with at least one unverified/unstated fact, or non-high "
        "confidence, are listed.\n"
    )
    any_listed = False
    current_domain = None
    for e in entries:
        vc = e.get("verification_confidence", {}) or {}
        overall = vc.get("overall", "low")
        declared = list(vc.get("unverified", []) or [])
        sentinels = [name for name, getter in VOLATILE if is_unstated(getter(e))]
        if overall == "high" and not declared and not sentinels:
            continue
        any_listed = True
        if e["domain"] != current_domain:
            current_domain = e["domain"]
            lines.append(f"\n### {current_domain}\n")
        bits = [f"**{e['name']}** (`{e['id']}`) — confidence: {overall}"]
        if sentinels:
            bits.append(f"unstated: {', '.join(sentinels)}")
        extra = [d for d in declared if d not in sentinels and d.split('.')[-1] not in {s.split('.')[-1] for s in sentinels}]
        if extra:
            bits.append(f"also flagged: {', '.join(extra)}")
        note = vc.get("notes")
        line = "- " + " — ".join(bits)
        if note:
            line += f"\n  - _note:_ {note}"
        lines.append(line)

    if not any_listed:
        lines.append("\n_All entries are high-confidence with every volatile fact grounded._\n")

    # Link check section.
    lines.append("\n## Link resolution\n")
    if LINKCHECK.exists():
        data = json.loads(LINKCHECK.read_text())
        summary = data.get("summary", {})
        lines.append(
            f"From the most recent `scripts/check_links.py` run: "
            + ", ".join(f"{k}={v}" for k, v in sorted(summary.items()))
            + ".\n"
        )
        guarded = [r for r in data.get("results", []) if r["status"] != "ok"]
        if guarded:
            lines.append(
                "These hosts answered but blocked the scripted request (HTTP "
                "401/403/405/429 — typically vendor/government anti-bot). The pages "
                "load in a browser; confirm manually:\n"
            )
            for r in guarded:
                lines.append(f"- {r['code']} — `{r['id']}` — {r['url']}")
        dead = [r for r in data.get("results", []) if r["status"] in ("unreachable", "http-error", "error")]
        if dead:
            lines.append("\n**Dead links needing a fix:**\n")
            for r in dead:
                lines.append(f"- `{r['id']}` — {r['url']}")
        else:
            lines.append("\nNo genuinely dead links were found.")
    else:
        lines.append("Run `python scripts/check_links.py --json linkcheck.json` first to populate this section.")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(REPO_ROOT)} ({n} entries, {sentinel_count} unstated fields)")
    return 0


if __name__ == "__main__":
    main()
