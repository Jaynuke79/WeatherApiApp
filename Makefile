# Variables
CHECK_DIR ?= .
PYTHONPATH := $(CHECK_DIR)/WeatherWizard
PYTHON_FILES := $(CHECK_DIR)/WeatherWizard/weather/*.py
PUML_DIR := $(CHECK_DIR)/uml
PUML_FILES := $(wildcard $(PUML_DIR)/*.puml)
PNG_FILES := $(PUML_FILES:.puml=.png)

# Targets
.PHONY: all style type-check test docs clean

all: plant style type-check test docs clean
	@echo "All checks passed"

test:
	PYTHONPATH=$(PYTHONPATH) python -m unittest discover -s tests
	PYTHONPATH=$(PYTHONPATH) coverage run -m unittest discover -s tests
	coverage report -m
	coverage html
	@echo "Open coverage report: file://$(shell pwd)/htmlcov/index.html"

style:
	flake8 --count --show-source --statistics $(PYTHONPATH)

type-check:
	mypy $(CHECK_DIR) --strict --allow-untyped-decorators --ignore-missing-imports

docs:
	pdoc --output-dir $(CHECK_DIR)/docs WeatherWizard/weather/weather.py 
	@echo "Documentation generated in $(CHECK_DIR)/docs/"
	@echo "Open $(CHECK_DIR)/docs/index.html in your browser to view the documentation"
	@echo "To view the documentation, run: open $(CHECK_DIR)/docs/index.html"

plant: $(PNG_FILES)

$(PUML_DIR)/%.png: $(PUML_DIR)/%.puml
	plantuml $<

	@echo "Cleaning up..."
	-find $(CHECK_DIR) -type d -name __pycache__ -exec rm -rf {} \; || true
	-find $(CHECK_DIR) -type d -name .pytest_cache -exec rm -rf {} \; || true
	-find $(CHECK_DIR) -type d -name .mypy_cache -exec rm -rf {} \; || true
	-find $(CHECK_DIR) -type d -name .hypothesis -exec rm -rf {} \; || true
	-find $(CHECK_DIR) -name .coverage -exec rm -f {} \; || true
	@echo "Cleanup complete"
