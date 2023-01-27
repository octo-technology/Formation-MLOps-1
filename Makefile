SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:
.SILENT:

.PHONY: help
help:
	echo "❓ Utiliser \`make <target>' où <target> peut être"
	grep -E '^\.PHONY: [a-zA-Z0-9_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: conda-env  ## 🐍 Créé l'environnement conda python_indus, et le récréé s'il existe déjà
conda-env:
	conda create --name python_indus python==3.10 --force --quiet; pip install -r requirements.txt

.PHONY: test-tps  ## lance les tests
test-tps:
	bats test.bats

.PHONY: sphinx  ## crée la documentation
sphinx:
	sphinx-build -b html docs docs/_build


.PHONY: distribution  ## crée le package
distribution:
	python3 setup.py sdist bdist_wheel
