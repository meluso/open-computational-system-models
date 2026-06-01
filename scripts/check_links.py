#!/usr/bin/env python3
"""Check that every entry's access_link and every source_per_field URL resolves.

Uses only the standard library so it runs anywhere. Does a HEAD, falling back to
a small GET, and treats common anti-bot responses (403/429/405) as "reachable but
guarded" rather than broken, because many vendor sites block scripted HEADs.

Usage:
    python scripts/check_links.py            # check access_link only
    python scripts/check_links.py --sources  # also check source_per_field URLs
    python scripts/check_links.py --json out.json
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from collections import Counter

from common import load_entries

URL_RE = re.compile(r"https?://[^\s)>\]]+")
UA = "Mozilla/5.0 (compatible; ocsm-linkcheck/1.0)"
TIMEOUT = 20
# Treat these as "reachable but guarded" — the host answered, just not 200.
GUARDED = {401, 403, 405, 429}


def check_url(url: str) -> tuple[str, int | None]:
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return ("ok", resp.status)
        except urllib.error.HTTPError as e:
            if e.code in GUARDED:
                return ("guarded", e.code)
            if method == "GET":
                return ("http-error", e.code)
            # else fall through to GET
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if method == "GET":
                return ("unreachable", None)
        except Exception:
            if method == "GET":
                return ("error", None)
    return ("unreachable", None)


def collect_urls(check_sources: bool) -> list[tuple[str, str, str]]:
    """Return (entry_id, where, url) tuples."""
    out = []
    for e in load_entries():
        eid = e.get("id", e.get("_stem", "?"))
        link = e.get("access_link")
        if link:
            out.append((eid, "access_link", link))
        if check_sources:
            spf = e.get("source_per_field", {}) or {}
            for field, val in spf.items():
                for m in URL_RE.findall(str(val)):
                    out.append((eid, f"source:{field}", m))
    return out


def main(argv: list[str]) -> int:
    check_sources = "--sources" in argv
    json_out = None
    if "--json" in argv:
        json_out = argv[argv.index("--json") + 1]

    targets = collect_urls(check_sources)
    # De-duplicate identical URLs to save requests.
    seen: dict[str, tuple[str, int | None]] = {}
    results = []
    counts: Counter = Counter()
    for eid, where, url in targets:
        if url not in seen:
            seen[url] = check_url(url)
        status, code = seen[url]
        counts[status] += 1
        results.append({"id": eid, "where": where, "url": url, "status": status, "code": code})
        flag = {"ok": "ok  ", "guarded": "gard", "http-error": "HTTP", "unreachable": "DEAD", "error": "ERR "}.get(status, "??  ")
        print(f"  [{flag}] {code or '   '} {eid} {where}: {url}")

    print()
    summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    print(f"Checked {len(results)} URL references: {summary}")

    if json_out:
        with open(json_out, "w", encoding="utf-8") as fh:
            json.dump({"summary": dict(counts), "results": results}, fh, indent=2)
        print(f"Wrote {json_out}")

    # Only hard failures (truly dead / http-error) cause a non-zero exit.
    broken = counts.get("unreachable", 0) + counts.get("http-error", 0) + counts.get("error", 0)
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
