SHELL := /bin/bash
.SILENT:

PYTHON_DIRS := src

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

.PHONY: test-notebook  ## exécute chaque notebook de notebook/ sur une copie isolée, sans modifier les modèles
test-notebook:
	uv run python scripts/run_notebook.py notebook

.PHONY: clean  ## supprime les fichiers générés (caches, build, doc) ; ne touche ni à .venv ni aux modèles
clean:
	rm -rf build dist docs/_build *.egg-info .pytest_cache .ruff_cache */__pycache__ */*/__pycache__ */.ipynb_checkpoints

.PHONY: tp2-validation  ## vérifie l'état de départ du TP2 (le notebook s'exécute de bout en bout)
tp2-validation: test-notebook
