# Acceptance Criteria

These are the concrete, checkable criteria this catalog is tested against. They are
written for the catalog's audience — **practicing professionals, engineers, and data
scientists** who would evaluate these models for real work. Each criterion names the
audience need it serves. Testing against these criteria is reported in
[`TEST_REPORT.md`](TEST_REPORT.md).

A criterion is **MUST** (a release blocker) or **SHOULD** (a quality target; misses
are explained, not hidden).

## 1. Inclusion integrity

- **A1 (MUST).** Every entry passes the executability test: it names specific
  `inputs_you_can_change` and specific `outputs_you_can_observe`, and the
  `executability_justification` states what a user varies and what observably changes.
  *Why: the catalog's core requirement is that an entry be "runnable," not merely "documented."*
- **A2 (MUST).** No entry is a purely static/descriptive artifact (e.g. a static DSM
  with no computation, a requirements matrix). *Why: those waste a professional's time
  here.*
- **A3 (SHOULD).** Each entry's `scale` reflects a representative model with more than
  25 interacting elements, or explains honestly why the element count is `unstated`.
  *Why: the working definition requires many interacting elements.*

## 2. Schema & data integrity (machine-checked by `validate.py`)

- **B1 (MUST).** Every entry validates against `schema/entry.schema.json` with zero
  errors. *Why: a skeptical reader must trust the data is well-formed.*
- **B2 (MUST).** These fields are present and non-empty on **every** entry: `name`,
  `gloss`, `domain`, `system_represented`, `inputs_you_can_change`,
  `outputs_you_can_observe`, `runtime_required`, `access_type`, `license`, `scale`,
  `maintenance_status`, `access_link`, `suitability`, `executability_justification`,
  `last_verified`, `source_per_field`, `verification_confidence`.
- **B3 (MUST).** `access_type` is present on every entry (it is recorded, never used
  as a filter). `last_verified` is a valid ISO date on every entry.
- **B4 (MUST).** Every `domain` value is in the registry; every `id` is unique and
  matches its filename.

## 3. Coverage

- **C1 (MUST).** Every one of the 17 core domain clusters in the brief has at least
  **2** qualifying entries, *unless* a documented note in `GAPS.md`/`PROGRESS.md`
  explains that the domain genuinely yields fewer. *Why: a catalog with few entries in a
  domain a professional cares about is not useful to them.*
- **C2 (MUST).** Every explicitly named seed model in the brief is either present as an
  entry or has a one-line note explaining its absence (e.g. fails the inclusion test).
  *Why: the brief's seeds are the minimum a knowledgeable reader will look for.*
- **C3 (SHOULD).** The catalog contains at least **80** entries total, going beyond the
  named seeds where a domain has many qualifying models. *Why: "seeds, not limits."*
- **C4 (SHOULD).** The full range of access types is represented (permissive-open
  through commercial and campus-or-employer-licensed). *Why: professionals use licensed
  tools too; the catalog must not be open-source-only.*

## 4. Accuracy & verifiability of volatile facts

- **D1 (MUST).** No volatile fact (version, license, maintenance status, element count)
  is invented. Anything not grounded in a source is the sentinel
  `unstated — needs direct verification` and is listed in
  `verification_confidence.unverified`. *Why: a confident wrong fact is worse than an
  honest gap for someone making decisions.*
- **D2 (MUST).** Every entry records `source_per_field` for its volatile facts and a
  `last_verified` date. *Why: the reader must be able to re-check.*
- **D3 (SHOULD).** Where feasible, version/license/maintenance facts are corroborated
  by a primary source (the project's own site, repository, or package registry).
- **D4 (MUST).** Every fact that is `unstated` or low-confidence appears in `GAPS.md`
  so the maintainer can do targeted manual checks.
- **D5 (MUST).** Maintenance currency is judged by whether the tool is usable and
  maintained *now*, not by origination date; anything dormant or abandoned is flagged
  via `maintenance_status.status`, not dropped silently.

## 5. The website (tested headlessly)

- **E1 (MUST).** `build.py` produces `site/index.html` and renders every valid entry as
  a structured card carrying the schema fields.
- **E2 (MUST).** The site supports **full-text search**, **filter by domain**, **filter
  by access type**, and **sort by maintenance recency**. *Why: these are exactly the
  ways a professional narrows a list of tools.* This is verified by
  `tests/test_site_logic.mjs` exercising the real site logic module.
- **E3 (MUST).** Search/filter/sort logic passes 100% of the headless tests.
- **E4 (SHOULD).** Each card shows access type, maintenance status, verification
  confidence, and last-verified date without opening the entry. *Why: these trust
  indicators must be visible without a click.*

## 6. Links

- **F1 (MUST).** Every entry has a syntactically valid `https?://` `access_link`.
- **F2 (SHOULD).** `access_link` URLs resolve (HTTP 200, or a guarded 401/403/405/429
  that indicates the host is alive). Any genuinely dead link is fixed or flagged in
  `GAPS.md`. *Why: a dead canonical link makes an entry useless.*

## 7. The prose documents (text-to-speech quality)

- **G1 (MUST).** Three documents exist: Part 1 (inventory by domain), Part 2
  (generative AI across these traditions), Part 3 (the intersection).
- **G2 (MUST).** Prose is TTS-friendly: flowing prose in short declarative sentences,
  no bullet inventories, no tables, no bold-label run-ins, minimal headers. Glosses
  appear in parentheses where a listener needs them.
- **G3 (SHOULD).** Acronyms are spelled out on first use in each document.
- **G4 (MUST).** Part 1 is rendered from the same data as the website, and its facts
  stay parallel across entries (same questions answered for each).

## 8. Reproducibility

- **H1 (MUST).** `make all` (validate, build, test) succeeds from a clean checkout
  after `make venv`, with no manual steps.
- **H2 (SHOULD).** The build is deterministic given the data (only the build date
  varies, and that is overridable via `BUILD_DATE`).
