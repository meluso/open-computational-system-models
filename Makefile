# Catalog of Computational System Models — task runner.
# Uses a local virtualenv so the build is reproducible.

PY := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: help venv validate build test test-site links gaps serve clean all

help:
	@echo "Targets:"
	@echo "  make venv      - create .venv and install deps (PyYAML, jsonschema)"
	@echo "  make validate  - validate every entry against the schema (exits non-zero on any error)"
	@echo "  make build     - validate, then render site/ and docs/"
	@echo "  make test      - run validation + headless site-logic tests"
	@echo "  make test-site - run the Node headless search/filter/sort tests"
	@echo "  make links     - check access_link URLs resolve (add SOURCES=1 for sources)"
	@echo "  make serve     - preview the built site over HTTP at localhost:8000"
	@echo "  make all       - validate, build, test"
	@echo "  make clean     - remove generated site/ output"

venv:
	python3 -m venv .venv
	$(PIP) install --quiet --upgrade pip
	$(PIP) install --quiet -r requirements.txt

validate:
	$(PY) scripts/validate.py

build:
	$(PY) scripts/build.py

test-site:
	node tests/test_site_logic.mjs

test: validate test-site
	@echo "All tests passed."

links:
	$(PY) scripts/check_links.py --json linkcheck.json $(if $(SOURCES),--sources,)

gaps:
	$(PY) scripts/gaps.py

# Serve the built site over HTTP. Open the page over http://, not file://,
# otherwise the browser blocks the ES-module imports and nothing renders.
serve:
	cd site && python3 -m http.server 8000

all: validate build test

clean:
	rm -rf site
