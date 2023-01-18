SHELL := /bin/sh
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