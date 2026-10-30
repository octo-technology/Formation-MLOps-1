SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:

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
	uv run ruff check src api tests docs

.PHONY: format  ## formate le code avec Ruff
format:
	uv run ruff format src api tests docs

.PHONY: static-validation  ## vérifie le lint et la mise en forme sans modifier le code
static-validation:
	uv run ruff check src api tests docs
	uv run ruff format --check src api tests docs

.PHONY: test  ## lance les tests Python
test:
	uv run python -m pytest

.PHONY: dependency-scan  ## analyse uv.lock avec Trivy (à installer séparément)
dependency-scan:
	trivy fs --config trivy.yaml .

.PHONY: test-notebook  ## exécute une copie du notebook sans modifier les modèles
test-notebook:
	tmp_dir=$$(mktemp -d)
	trap 'rm -rf "$$tmp_dir"' EXIT
	trap 'exit 130' INT
	trap 'exit 143' TERM
	mkdir -p "$$tmp_dir/notebook" "$$tmp_dir/models"
	cp notebook/titanic.ipynb "$$tmp_dir/notebook/"
	ln -s "$$PWD/input" "$$tmp_dir/input"
	uv run jupyter nbconvert --to notebook --execute \
		"$$tmp_dir/notebook/titanic.ipynb" \
		--output executed --output-dir "$$tmp_dir"

.PHONY: test-tps  ## valide le notebook, les tests, le package et la documentation
test-tps:
	tmp_dir=$$(mktemp -d)
	trap 'rm -rf "$$tmp_dir"' EXIT
	trap 'exit 130' INT
	trap 'exit 143' TERM
	$(MAKE) test-notebook
	$(MAKE) test
	$(MAKE) distribution DIST_OUTPUT_DIR="$$tmp_dir/dist"
	$(MAKE) sphinx SPHINX_OUTPUT_DIR="$$tmp_dir/html"

.PHONY: sphinx  ## crée la documentation
sphinx:
	uv run sphinx-build -W -b html docs "$(SPHINX_OUTPUT_DIR)"


.PHONY: distribution  ## crée le package
distribution:
	uv build --out-dir "$(DIST_OUTPUT_DIR)"
