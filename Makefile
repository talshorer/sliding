PYTHON ?= python3
export PYTHON

all: pycheck test

test:
	$(PYTHON) tests/autotest.py

pycheck:
	scripts/pycheck.sh
