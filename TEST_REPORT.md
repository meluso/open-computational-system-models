# Test Report

Results of testing the catalog against [`ACCEPTANCE.md`](ACCEPTANCE.md). Run date:
2026-06-01. Catalog size at test time: **89 entries** across **19 domains** (the 17
core clusters plus two adjacent ones).

How to reproduce: `make venv && make all && make links && make gaps`.

## Summary

| Area | Result |
|---|---|
| Schema validation (`validate.py`) | **PASS** — 89 entries, 0 errors, 0 warnings |
| Build (`build.py`) | **PASS** — `site/` + `docs/part1–3.md` rendered |
| Headless site search/filter/sort (`tests/test_site_logic.mjs`) | **PASS** — 21/21 |
| Link resolution (`check_links.py`) | **PASS** — 89 checked, 77×200, 12 guarded, **0 dead** |
| Coverage (≥2 per core domain, ≥80 entries) | **PASS** |
| Honesty of volatile facts | **PASS** — 0 invented; 41 fields marked `unstated`, all flagged |

## Criterion-by-criterion

### 1. Inclusion integrity
- **A1 (MUST) PASS.** Every entry has non-empty `inputs_you_can_change`,
  `outputs_you_can_observe`, and an `executability_justification` stating what a
  user varies and what observably changes (enforced by schema `minItems`/`minLength`).
- **A2 (MUST) PASS.** No purely static artifacts. The two DSM entries are the
  *computing* kind (they cluster/sequence a matrix); a static DSM was deliberately
  not included. Static SysML and EAST-ADL/EATOP tooling were excluded (see GAPS).
- **A3 (SHOULD) PASS.** Every `scale.element_count` either describes a
  representative >25-element model or carries the `unstated` sentinel. No entry has a
  plain element count ≤25 (validator warns on that; none fired).

### 2. Schema & data integrity
- **B1 (MUST) PASS.** 89/89 validate against `schema/entry.schema.json`, 0 errors.
- **B2 (MUST) PASS.** All mandatory fields present and non-empty on every entry
  (schema `required` + `minLength`/`minItems`).
- **B3 (MUST) PASS.** `access_type` present on all 89; `last_verified` is a valid
  ISO date on all 89.
- **B4 (MUST) PASS.** All `domain` values are in the registry; all 89 `id`s are
  unique and match their filenames (cross-checked by `validate.py`).

### 3. Coverage
- **C1 (MUST) PASS.** All 17 core clusters have ≥2 entries. Smallest core domains:
  circuits-electronics (2), architecture-description-langs (2), computing-dsm (2). The
  two *adjacent* domains have 1 each (systems-biology-sbml, continuum-cfd), which is
  in scope per the brief's "include only where framable" framing and is documented.
- **C2 (MUST) PASS.** Every explicitly named seed is present **or** has a recorded
  reason for absence. Documented absences: **EAST-ADL** (EATOP is an editing platform
  without a built-in runnable analysis engine and appears dormant); the **Clarkson/
  Eckert change-propagation DSM** (no maintained public runnable implementation found —
  clustering DSMs are included instead); a standalone **rocket delta-V spreadsheet**
  (no stable public download confirmed; the fuel-economy/budget spreadsheet need is met
  by GREET, the AMSAT link budget, and the Artemis CubeSat power budget). See `GAPS.md`.
- **C3 (SHOULD) PASS.** 89 entries (target ≥80).
- **C4 (SHOULD) PASS.** Access spectrum is broad: permissive-open 51, copyleft-open
  11, weak-copyleft-open 8, campus-or-employer-licensed 12, commercial 4, free-closed 2,
  freemium 1. Full range represented.

### 4. Accuracy & verifiability
- **D1 (MUST) PASS.** No volatile fact was invented. 41 fields carry the explicit
  `unstated — needs direct verification` sentinel; each is reflected in the entry's
  `verification_confidence` (validator cross-checks this and reported 0 warnings).
- **D2 (MUST) PASS.** Every entry has `source_per_field` and a `last_verified` date.
- **D3 (SHOULD) PASS (mostly).** 62/89 entries are high-confidence with volatile
  facts grounded in a primary source (PyPI JSON, GitHub releases API, or project site).
  27 are medium — chiefly the commercial tools (Dymola, MapleSim, Amesim, GT-SUITE,
  AnyLogic) whose vendor pages publish neither version nor license, and a few dormant or
  spreadsheet artifacts. None are low.
- **D4 (MUST) PASS.** `GAPS.md` lists every unstated/medium-confidence fact, grouped
  by domain, and is regenerated from the data by `scripts/gaps.py`.
- **D5 (MUST) PASS.** Maintenance is judged by recent activity, not origination.
  Dormant/abandoned tools are flagged via `maintenance_status.status` (e.g. Ptolemy II,
  SUAVE, the two DSM tools, tep2py) rather than dropped.

### 5. The website
- **E1 (MUST) PASS.** `build.py` produced `site/index.html` and renders all 89
  entries as structured cards carrying the schema fields.
- **E2 (MUST) PASS.** Full-text search, filter-by-domain, filter-by-access-type, and
  sort-by-maintenance-recency are implemented in `web/catalog-logic.mjs` and confirmed
  against the **real generated catalog** (e.g. search "wind" → 25 hits; filter
  power-energy → 10; filter commercial → 4; recency sort top = MuJoCo 2026-05-27).
- **E3 (MUST) PASS.** 21/21 headless assertions pass; the test imports the exact
  module the browser uses.
- **E4 (SHOULD) PASS.** Each card shows domain, access type, maintenance status,
  verification-confidence, and last-verified date as badges/footer.

### 6. Links
- **F1 (MUST) PASS.** All 89 `access_link`s are syntactically valid `https?://` URLs.
- **F2 (SHOULD) PASS.** 89 checked: 77 return HTTP 200; 12 are "guarded" (HTTP 403)
  — all MathWorks documentation/File-Exchange pages (11) and Argonne GREET (1), which
  block scripted requests but load in a browser. **Zero genuinely dead links.**

### 7. The prose documents
- **G1 (MUST) PASS.** `docs/part1.md` (inventory by domain), `docs/part2.md`
  (generative AI across the traditions), `docs/part3.md` (the intersection) all exist.
- **G2 (MUST) PASS.** Prose is flowing and declarative with no bullet inventories,
  tables, or bold-label run-ins; glosses appear in parentheses on first mention.
- **G3 (SHOULD) PASS (with caveat).** Acronyms are spelled out on first use in the
  authored domain lead-ins and essays (M B S E, M D O, A I, etc.) and in most entry
  glosses. A few entry-level glosses harvested from sources may use an acronym before its
  expansion; these are isolated and low-impact for a listener.
- **G4 (MUST) PASS.** Part 1 is rendered programmatically from the same entries as
  the website, with parallel facts per model.

### 8. Reproducibility
- **H1 (MUST) PASS.** `make venv && make all` succeeds from a clean checkout.
- **H2 (SHOULD) PASS.** The build is deterministic given the data; only the build
  date varies and is overridable via `BUILD_DATE`.

## Failures and what was done about them

No MUST criterion failed. Items worth the maintainer's attention:

1. **27 medium-confidence entries.** Concentrated in commercial tools whose vendors do
   not publish versions or license terms on public pages. Marked honestly as `unstated`
   and listed in `GAPS.md`. Action taken: did not guess.
2. **12 guarded links (HTTP 403).** All MathWorks / GREET anti-bot responses, not dead
   links. Action taken: classified separately by the link checker and listed in
   `GAPS.md` for quick manual confirmation in a browser.
3. **Two adjacent domains have a single entry each** (SBML, CFD). By design — they are
   adjacent and included only where framable as a runnable multi-element system.
4. **Three documented seed absences** (EAST-ADL, change-propagation DSM, standalone
   rocket delta-V spreadsheet), explained under C2 and in `GAPS.md`.
