SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:

.PHONY: help
help:
	echo "❓ Utiliser \`make <target>' où <target> peut être"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: install  ## 📦 Installe les dépendances avec uv
install:
	uv sync

.PHONY: lint  ## 🔍 Lance le linting (ruff, safety, bandit, vulture)
lint:
	uv run ruff check src tests
	uv run bandit -r src
	uv run vulture src --min-confidence 80

.PHONY: test  ## 🧪 Lance les tests unitaires
test:
	uv run pytest tests

.PHONY: test-tps  ## lance les tests
test-tps:
	bats test.bats

.PHONY: sphinx  ## crée la documentation
sphinx:
	uv run sphinx-build -b html docs docs/_build


.PHONY: distribution  ## crée le package
distribution:
	uv build
