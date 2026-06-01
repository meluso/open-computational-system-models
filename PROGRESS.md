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
  consistency, a soft >25-element inclusion warning). Fails loudly with non-zero exit.
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

## Stage C — Populate the catalog  ⏳ (in progress)

(Updated as entries land.)
