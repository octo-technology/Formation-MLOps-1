SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:

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

.PHONY: test-tps  ## valide les TP avec Bats (à installer séparément)
test-tps:
	bats test.bats

.PHONY: sphinx  ## crée la documentation
sphinx:
	uv run sphinx-build -W -b html docs docs/_build/html


.PHONY: distribution  ## crée le package
distribution:
	uv build
