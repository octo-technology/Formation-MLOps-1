SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:

.PHONY: help
help:
	echo "❓ Utiliser \`make <target>' où <target> peut être"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: notebook-validation  ## 🔭 Lance le notebook titanic.ipynb pour s'assurer qu'il peut être exécuté de bout en bout
notebook-validation:
	uv run jupyter nbconvert --to script notebook/titanic.ipynb
	cd notebook
	uv run python titanic.py

.PHONY: tp-validation  ## 1️⃣ Valide que le notebook est bien clean
tp-validation:
	$(MAKE) notebook-validation 2>execution_output.log || true
	status=$$?
	execution_output=$$(cat execution_output.log && rm -f execution_output.log)
	rm notebook/y_test_predictions.csv
	rm notebook/titanic.py
	echo "-----------------------"
	echo "$$execution_output"
	echo "-----------------------"
	if [ $$status -eq 0 ];
	then
		echo "✅ Le notebook a réussi a run de bout en bout";
		exit 0
	else
		echo "❌ Le notebook a échoué a run de bout en bout"
		exit 1
	fi

.PHONY: install  ## 📦 Installe les dépendances avec uv
install:
	uv sync

.PHONY: install-hooks  ## Installe les git hooks (pre-commit)
install-hooks:
	chmod +x .githooks/pre-commit  # ok pour windows s'ils utilisent git bash
	git config core.hooksPath .githooks

.PHONY: pre-commit  ## 🔄 Lance le pre-commit manuellement
pre-commit:
	.githooks/pre-commit

.PHONY: lint  ## 🔍 Lance le linting (ruff, safety, bandit, vulture)
lint:
	uv run ruff check src tests
	uv run bandit -r src
	uv run vulture src --min-confidence 80

.PHONY: test  ## 🧪 Lance les tests unitaires
test:
	uv run pytest tests
