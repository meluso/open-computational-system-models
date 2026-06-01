# Progress Log

A running account of the build, kept current as work proceeds. Newest section last.

## Conventions decided up front

- **Audience:** practicing professionals, engineers, and data scientists. Every
  judgment call resolves toward what a skeptical senior engineer evaluating these
  models for real work would need.
- **Scope (confirmed with the owner):** ~80–100 entries — all named seeds plus clear
  additions per domain, with deep per-entry verification.
- **Honesty (confirmed with the owner):** any volatile fact not groundable in a source
  gets the sentinel `unstated — needs direct verification`, is reflected in
  `verification_confidence`, and is logged in `GAPS.md`. Never guess.

## Stage A — Schema and acceptance criteria  ✅

- Designed the entry schema as `schema/entry.schema.json` (JSON Schema draft-07).
  Includes every field the brief mandates plus `id` (stable identifier / filename
  stem), `executability_justification` (forces the inclusion test to be argued per
  entry), and `tags`. Volatile fields accept the explicit `unstated` sentinel.
  `access_type` and `last_verified` are mandatory. `verification_confidence` carries an
  explicit `unverified` list.
- Built the domain registry `data/domains.yml` — the 17 core clusters plus two
  adjacent ones (systems-biology SBML, continuum/CFD) included only where framable as a
  runnable multi-element system.
- Wrote `ACCEPTANCE.md`: concrete MUST/SHOULD criteria, each justified by the audience.
  These are what Stage E tests against.

## Stage B — Scaffold  ✅

- `scripts/validate.py`: schema validation + cross-entry rules (id uniqueness,
  id/filename match, domain in registry, ISO date check, unstated-vs-declared
  consistency, a soft >25-element inclusion warning). Exits non-zero with explicit errors.
- `scripts/build.py`: validates first, then renders the website (`site/`) and the three
  prose documents (`docs/`) from the same data. Refuses to build on invalid data.
- `web/`: hand-written site source. `catalog-logic.mjs` is a pure module shared by the
  browser app and the headless test. Generated data is emitted as an ES module so the
  site runs from `file://`.
- `tests/test_site_logic.mjs`: 21 headless assertions over the real search/filter/sort
  logic. `scripts/check_links.py`: standard-library link checker. `Makefile`,
  `requirements.txt`, `.gitignore`, `README.md` (with tech-stack justification).
- **Pipeline verified end-to-end** on a first grounded entry (OpenMDAO, facts confirmed
  against PyPI): validate ✅, build ✅, site tests 21/21 ✅.

## Stage C — Populate the catalog  ✅

- **Method.** Ran parallel domain research across the 17 core clusters plus the
  two adjacent ones. Each research pass produced schema-shaped entries with per-field
  source URLs and an honest `verification_confidence`, verifying volatile facts against
  PyPI JSON, GitHub releases, and project/vendor sites. A one-time `scripts/ingest.py`
  parsed the returned blocks, stripped any keys outside the schema, stringified
  YAML-autoparsed dates, deduped by id, and wrote clean per-entry YAML. The bulky raw
  research dumps are not committed (the canonical source is `data/entries/*.yml`; each
  entry's `source_per_field` is the audit trail).
- **Result: 89 entries.** By domain — mathworks-mbd 11, power-energy 10, des-abm 8,
  equation-based-physical 7, robotics-multibody 7, mdo 6, aerospace-space 5,
  heterogeneous-digital-twin 5, executable-mbse 4, controls-dynamics-python 4,
  infrastructure-networks 4, wind-marine-energy 4, process-chemical 3,
  parametric-spreadsheets 3, circuits-electronics 2, architecture-description-langs 2,
  computing-dsm 2, systems-biology-sbml 1, continuum-cfd 1.
- **Honesty.** 62 entries high-confidence, 27 medium, 0 low. 41 volatile fields carry
  the explicit `unstated` sentinel — chiefly the commercial tools (Dymola, MapleSim,
  Amesim, GT-SUITE) whose vendors publish no public version/license, and a few dormant
  or spreadsheet artifacts. Nothing was guessed.
- **Key decisions.** (1) WISDEM appeared from two research passes (MDO and wind);
  kept the better-grounded wind-marine-energy entry, dropped the duplicate. (2) WEC-Sim
  recorded as `campus-or-employer-licensed` because, although the code is Apache-2.0, it
  cannot run without MATLAB/Simulink — access reflects what it takes to *run* it.
  (3) MathWorks reference apps recorded as `campus-or-employer-licensed` for the same
  reason, even though the files are free to download. (4) Documented seed absences:
  EAST-ADL (no runnable analysis engine; dormant), Clarkson change-propagation DSM (no
  maintained public runnable implementation), standalone rocket delta-V spreadsheet (no
  stable public download confirmed).

## Stage D — Narrative prose  ✅

- `scripts/build.py` renders all three documents from the same data. **Part 1** is a
  true data render: a TTS-friendly inventory, by domain, with parallel facts per model,
  authored domain lead-ins that spell out acronyms, and glosses in parentheses. **Part 2**
  (generative AI across the traditions) and **Part 3** (the intersection of open runnable
  models and AI) are authored essays whose few figures (entry counts, open-vs-licensed
  split) are injected from the live catalog so they stay consistent with the data.
- Style holds to the brief: flowing short declarative sentences, no bullets/tables/
  bold run-ins, minimal headers.

## Stage E — Test and report  ✅

- `make all` is green: validate (89/0/0), build, and 21/21 headless site-logic tests.
- Link check: 89 `access_link`s, 77×HTTP 200, 12 guarded (MathWorks + GREET anti-bot
  403s — live in a browser), **0 dead**.
- Wrote `TEST_REPORT.md` (every ACCEPTANCE criterion, with results) and `GAPS.md`
  (generated by `scripts/gaps.py` from the data + link-check JSON).

## Open questions for you

1. **Commercial-tool facts.** Dymola, MapleSim, Simcenter Amesim, and GT-SUITE have
   `unstated` version/license because the vendors publish neither publicly. If you have
   institutional access, those are the highest-value manual fills (see `GAPS.md`).
2. **Spreadsheet longevity.** The three spreadsheet entries point at real, reachable
   files, but versions/licenses are mostly `unstated`. Worth a manual look if spreadsheets
   are a priority domain for you; I kept only links I could confirm resolve.
3. **Adjacent domains.** SBML and CFD have one entry each by design. Say the word if
   you want them expanded into fuller sections or dropped.
4. **Element counts.** For framework-style tools, `scale.element_count` describes a
   representative model rather than a fixed number — the honest answer for tools that
   model arbitrary-size systems. Confirm that framing matches your intent.
