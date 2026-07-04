PYTHON ?= python

.PHONY: init dev-install demo test lint

init:
	@echo "Instalando dependencias de producción..."
	$(PYTHON) -m pip install -e .

dev-install:
	@echo "Instalando dependencias de desarrollo (pytest, linters)..."
	$(PYTHON) -m pip install -e .[dev]

demo:
	@echo "Ejecutando demo end-to-end con MockMotor..."
	$(PYTHON) -m antigravity_wings.scripts.demo_pipeline

test:
	@echo "Ejecutando tests (requiere: make dev-install primero)..."
	$(PYTHON) -m pytest -v

lint:
	@echo "Ejecutando verificaciones de calidad con ruff y mypy..."
	$(PYTHON) -m ruff check .
	$(PYTHON) -m mypy .
