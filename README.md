# Formation MLOps 1 : Industrialisation de la Data Science

Cette formation utilise Python 3.15 ou une version ultérieure, uv 0.13.5 pour gérer l'environnement et Ruff pour vérifier et formater le code.

Après avoir installé [uv](https://docs.astral.sh/uv/getting-started/installation/), exécutez les commandes suivantes depuis la racine du dépôt :

```sh
uv sync --locked
uv run jupyter lab
```

Les instructions des TP sont publiées sur les pages GitHub suivantes :

[TP 0 Installation de l'environnement](https://octo-technology.github.io/Formation-MLOps-1/tp0#0)

[TP 1 Nettoyer le notebook](https://octo-technology.github.io/Formation-MLOps-1/tp1#0)

[TP 2 Écrire des tests unitaires](https://octo-technology.github.io/Formation-MLOps-1/tp2#0)

[TP 3 Documenter avec Sphinx](https://octo-technology.github.io/Formation-MLOps-1/tp3#0)

[TP 4 Écrire un script de CI](https://octo-technology.github.io/Formation-MLOps-1/tp4#0)

[TP 5 Créer un package Python](https://octo-technology.github.io/Formation-MLOps-1/tp5#0)

[TP 6 Créer une API et la conteneuriser](https://octo-technology.github.io/Formation-MLOps-1/tp6#0)

## Vérifier la branche de développement

```sh
uv run ruff check src api tests docs
uv run ruff format --check src api tests docs
uv run python -m pytest
uv run sphinx-build -W -b html docs docs/_build/html
uv build
```

Les mêmes tâches sont disponibles via le `Makefile`. Pour exécuter les validations de TP de `test.bats`, installez [Bats](https://bats-core.readthedocs.io/en/stable/installation.html), puis lancez `make test-tps`. Elles utilisent des répertoires temporaires pour préserver les modèles et les fichiers du dépôt.
