# A Catalog of Computational System Models

A curated, verifiable catalog of **computational system models** — representations of
engineered systems with many interacting elements (more than twenty-five) that a
person can actually *run*, such that changing inputs or parameters produces
observably different outcomes.

The catalog lives as data (YAML) and renders to **both** a static website and three
narrative prose documents from that single source. It is built for practicing
professionals, engineers, and data scientists evaluating these models for real work.

## The one inclusion test

**Executability.** An entry qualifies only if a user can vary inputs or parameters
and observe changed outputs. Purely descriptive or static artifacts (a static design
structure matrix with no analysis, a requirements traceability matrix, a Quality
Function Deployment house of quality) do not qualify. Access type — from permissively
open to commercially licensed — is *recorded, never used as a filter*.

## Repository layout

```
data/
  domains.yml          # the domain registry (controls ordering everywhere)
  entries/*.yml        # one YAML file per model — the single source of truth
schema/
  entry.schema.json    # JSON Schema (draft-07) every entry must satisfy
scripts/
  common.py            # shared loaders
  validate.py          # schema + cross-entry validation; fails loudly
  build.py             # renders site/ and docs/ from data/ (validates first)
  check_links.py       # checks access_link / source URLs resolve
web/                   # hand-written site source (html, css, ES modules)
site/                  # GENERATED static website (committed artifact)
docs/                  # GENERATED prose: part1.md, part2.md, part3.md
tests/
  test_site_logic.mjs  # headless test of the site's search/filter/sort
ACCEPTANCE.md          # the acceptance criteria this catalog is tested against
TEST_REPORT.md         # results of testing against ACCEPTANCE.md
GAPS.md                # every fact that could not be verified
PROGRESS.md            # running build log and decisions
```

## Why these choices

**One file per entry** (not one file per domain). Engineering catalogs grow by
accretion and by many hands. One file per entry gives clean diffs, lets entries be
added or revised without merge conflicts, makes per-entry provenance obvious, and
lets parallel research write independently. The domain is a field on each entry, so
re-homing an entry is a one-line change, and the website and prose group by that
field at build time.

**Plain YAML data + a JSON Schema.** YAML is readable and reviewable by humans, and a
JSON Schema gives a single, machine-checkable definition of "valid entry." Validation
fails loudly (non-zero exit, explicit messages) so a malformed or under-specified
entry can never reach the website.

**Static site: vanilla HTML + ES modules, no framework, no build step for the JS.**
A skeptical senior engineer should be able to open the site, read the source, and
trust it. There is no bundler, no transpile, no npm dependency tree. The non-trivial
logic (search, filter, sort) lives in one pure ES module, `web/catalog-logic.mjs`,
which is imported *both* by the browser app and by the headless Node test — so the
test exercises exactly the code the site runs. The generated data is emitted as an ES
module (`catalog-data.mjs`), so the site works straight from `file://` with no server
and no fetch/CORS friction.

**Python for tooling.** Validation and rendering need only the standard library plus
PyYAML and jsonschema. No web framework, nothing to host, fully headless.

## Build, validate, test

```bash
make venv       # create .venv, install PyYAML + jsonschema
make validate   # validate every entry against the schema (fails loudly)
make build      # validate, then render site/ and docs/
make test       # validation + headless site-logic tests (Node)
make links      # check that access_link URLs resolve (SOURCES=1 to also check sources)
make all        # validate + build + test
```

Open `site/index.html` directly in a browser, or serve `site/` with any static host
(e.g. GitHub Pages). The site supports full-text search and filtering by domain and by
access type, and sorting by maintenance recency, name, or domain.

## Honesty about volatile facts

Element counts, licenses, versions, and maintenance status drift and are often left
unstated by sources. Every entry records `last_verified` (the date its volatile facts
were checked), `source_per_field` (where each came from), and an honest
`verification_confidence`. Where a fact could not be grounded in a source, the entry
carries the explicit sentinel **`unstated — needs direct verification`** rather than a
guess, and the fact is logged in [`GAPS.md`](GAPS.md).
