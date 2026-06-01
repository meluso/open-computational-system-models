# Catalog of Computational System Models — task runner.
# Uses a local virtualenv so the build is reproducible.

PY := .venv/bin/python
PIP := .venv/bin/pip

.PHONY: help venv validate build test test-site links clean all

help:
	@echo "Targets:"
	@echo "  make venv      - create .venv and install deps (PyYAML, jsonschema)"
	@echo "  make validate  - validate every entry against the schema (fails loudly)"
	@echo "  make build     - validate, then render site/ and docs/"
	@echo "  make test      - run validation + headless site-logic tests"
	@echo "  make test-site - run the Node headless search/filter/sort tests"
	@echo "  make links     - check access_link URLs resolve (add SOURCES=1 for sources)"
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
	$(PY) scripts/check_links.py $(if $(SOURCES),--sources,)

all: validate build test

clean:
	rm -rf site
