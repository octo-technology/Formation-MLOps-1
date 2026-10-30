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

Les mêmes tâches sont disponibles via le `Makefile` : `make static-validation`, `make test`, `make sphinx` et `make distribution`.

Avec GNU Make et Bash disponibles, lancez `make test-tps` pour vérifier successivement l'exécution du notebook, les tests Python, la construction du package et la documentation. La validation s'arrête au premier échec. Le notebook est exécuté sur une copie et les sorties sont placées dans des répertoires temporaires, nettoyés même en cas d'échec, pour préserver les notebooks et modèles du dépôt. `make test-notebook` permet de vérifier uniquement le notebook.

Pour les constructions autonomes, les sorties restent dans `dist/` et `docs/_build/html/`. Vous pouvez choisir d'autres répertoires avec `make distribution DIST_OUTPUT_DIR="chemin/dist"` et `make sphinx SPHINX_OUTPUT_DIR="chemin/html"`.
