SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:

.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: ls-supports  ## liste les supports de formation dispo sur gslide et en pdf selon la VERSION={v1.3, ...}
ls-supports:
	if [ -z "${VERSION}" ]
	then
		git config -f manifest.ini --list
	else
		git config -f manifest.ini --get-regexp ${VERSION}
	fi

.PHONY: install  ## 📦 Installe les dépendances avec uv
install:
	uv sync


.PHONY: notebook-validation  ## 🔭 Lance le notebook titanic.ipynb pour s'assurer qu'il peut être exécuté de bout en bout
notebook-validation:
	uv run jupyter nbconvert --to notebook --execute notebook/titanic.ipynb

.PHONY: tp-validation  ## 1️⃣ Valide que le TP1 est fonctionnel. L'import de pandas dans le notebook doit échouer.
tp-validation:
	$(MAKE) notebook-validation 2>execution_output.log || true
	execution_output=$$(cat execution_output.log && rm -f execution_output.log)
	echo "Le notebook a été exécuté de bout en bout:"
	echo "-----------------------"
	echo "$$execution_output"
	echo "-----------------------"
	if echo "$$execution_output" | grep -q "NameError.*pd.*";
	then
		echo "✅ L'import de Pandas a échoué comme prévu, le notebook du TP1 fonctionne comme prévu";
		exit 0
	else
		echo "❌ L'import de Pandas a réussi alors qu'il devrait normalement échouer"
		echo "❌ C'est l'objectif du TP de nettoyer le notebook après tout"
		exit 1
	fi
