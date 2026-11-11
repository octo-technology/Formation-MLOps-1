SHELL := /bin/bash
.SILENT:

PYTHON_DIRS := src api tests docs
SPHINX_OUTPUT_DIR ?= docs/_build/html
DIST_OUTPUT_DIR ?= dist

.PHONY: help
help:
	echo "❓ Utiliser \`make <target>' où <target> peut être"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: sync  ## installe l'environnement et les dépendances verrouillées
sync:
	uv sync --locked

.PHONY: lint  ## vérifie le code avec Ruff
lint:
	uv run ruff check $(PYTHON_DIRS)

.PHONY: format  ## formate le code avec Ruff
format:
	uv run ruff format $(PYTHON_DIRS)

.PHONY: test  ## lance les tests Python
test:
	uv run python -m pytest

.PHONY: install-hooks  ## installe le hook git pre-commit (vérification statique et tests avant chaque commit)
install-hooks:
	git config core.hooksPath .githooks && echo "✅ Hook pre-commit installé (.githooks/pre-commit)"

.PHONY: static-validation  ## vérifie le code sans le modifier (Ruff, Bandit et Vulture, comme la CI)
static-validation: lint
	uv run ruff format --check $(PYTHON_DIRS)
	uv run bandit -q -r src
	uv run vulture src --min-confidence 80

.PHONY: dependency-scan  ## analyse uv.lock avec Trivy (à installer séparément)
dependency-scan:
	trivy fs --config trivy.yaml .

.PHONY: sphinx  ## crée la documentation
sphinx:
	uv run sphinx-build -W -b html docs "$(SPHINX_OUTPUT_DIR)"

.PHONY: distribution  ## crée le package
distribution:
	uv build --out-dir "$(DIST_OUTPUT_DIR)"

.PHONY: test-notebook  ## exécute chaque notebook de notebook/ sur une copie isolée, sans modifier les modèles
test-notebook:
	uv run python scripts/run_notebook.py notebook

.PHONY: clean  ## supprime les fichiers générés (caches, build, doc) ; ne touche ni à .venv ni aux modèles
clean:
	rm -rf build dist docs/_build *.egg-info .pytest_cache .ruff_cache */__pycache__ */*/__pycache__ */.ipynb_checkpoints

.PHONY: test-tps  ## valide les notebooks, les tests, le package et la documentation
test-tps: test-notebook test
	tmp_dir=$$(mktemp -d) && trap 'rm -rf "$$tmp_dir"' EXIT && \
	$(MAKE) distribution DIST_OUTPUT_DIR="$$tmp_dir/dist" && \
	$(MAKE) sphinx SPHINX_OUTPUT_DIR="$$tmp_dir/html"
