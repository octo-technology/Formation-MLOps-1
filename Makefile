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
	jupyter nbconvert --to notebook --execute notebook/titanic.ipynb

.PHONY: tp-validation  ## 1️⃣ Valide que le notebook est bien clean
tp2-validation:
	$(MAKE) notebook-validation 2>execution_output.log || true
	execution_output=$$(cat execution_output.log && rm -f execution_output.log)
	rm notebook/titanic.nbconvert.ipynb
	rm notebook/y_test_predictions.csv
	echo "Le notebook a été exécuté de bout en bout:"
	echo "-----------------------"
	echo "$$execution_output"
	echo "-----------------------"
	## Si l'output contient...
	if [[ $$execution_output =~ "bytes to notebook/titanic.nbconvert.ipynb" ]];
	then
		echo "✅ Le notebook a réussi a run de bout en bout";
		exit 0
	else
		echo "❌ Le notebook a échoué a run de bout en bout"
		exit 1
	fi