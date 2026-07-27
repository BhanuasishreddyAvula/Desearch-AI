# Makefile for Desearch AI Backend Service

.PHONY: help install format lint typecheck quality run clean

PYTHON = python
UVICORN = uvicorn

help:
	@echo "Desearch AI Backend Development Commands:"
	@echo "  make install    Install backend dependencies"
	@echo "  make format     Format codebase with Black and isort"
	@echo "  make lint       Run Ruff linter checks"
	@echo "  make typecheck  Run mypy static type checking"
	@echo "  make quality    Run format, lint, and typecheck in sequence"
	@echo "  make run        Start development server"
	@echo "  make clean      Remove build artifacts and pycache"

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

format:
	isort app --settings-path pyproject.toml
	black app --config pyproject.toml

lint:
	ruff check app --config pyproject.toml

typecheck:
	mypy app --config-file pyproject.toml

quality: format lint typecheck

run:
	uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

clean:
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('.mypy_cache')]"
	$(PYTHON) -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('.ruff_cache')]"
