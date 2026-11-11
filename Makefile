SHELL := /bin/bash
.SILENT:

.PHONY: help
help:
	echo "❓ Utiliser \`make <target>' où <target> peut être"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: sync  ## installe l'environnement et les dépendances verrouillées
sync:
	uv sync --locked

.PHONY: tp1-validation  ## vérifie l'état de départ du TP1 (le notebook doit échouer sur l'import manquant de pandas)
tp1-validation:
	uv run python scripts/run_notebook.py --expect-error "NameError: name 'pd' is not defined" notebook/titanic.ipynb
