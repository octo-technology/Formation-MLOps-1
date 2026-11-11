# Formation MLOps 1 : Industrialisation de la Data Science

Cette formation utilise Python 3.15 ou une version ultérieure, uv 0.13.5 pour gérer l'environnement et Ruff pour vérifier et formater le code.

Après avoir installé [uv](https://docs.astral.sh/uv/getting-started/installation/), exécutez les commandes suivantes depuis la racine du dépôt :

```sh
uv sync --locked
uv run jupyter lab
```

### Les slides de la formation
**Version courante : v1.13** :arrow_right: [Google Slides](https://docs.google.com/presentation/d/1Gqgs0yIp0Fq2Vr_496sL3EuBiLaXJQtVqciYcu2q7OQ/edit?usp=sharing)


Les instructions des TP sont publiées sur les pages GitHub suivantes :

[TP 0 Installation de l'environnement](https://octo-technology.github.io/Formation-MLOps-1/tp0#0)

[TP 1 Nettoyer le notebook](https://octo-technology.github.io/Formation-MLOps-1/tp1#0)

[TP 2 Écrire des tests unitaires](https://octo-technology.github.io/Formation-MLOps-1/tp2#0)

[TP 3 Documenter avec Sphinx](https://octo-technology.github.io/Formation-MLOps-1/tp3#0)

[TP 4 Écrire un script de CI](https://octo-technology.github.io/Formation-MLOps-1/tp4#0)

[TP 5 Créer un package Python](https://octo-technology.github.io/Formation-MLOps-1/tp5#0)

[TP 6 Créer une API et la conteneuriser](https://octo-technology.github.io/Formation-MLOps-1/tp6#0)

## Contribuer

Le guide de contribution ([CONTRIBUTING.md](CONTRIBUTING.md)) décrit l'organisation des branches, les conventions de commit et le déroulé d'une contribution.

## Vérifier la branche de développement

```sh
# make static-validation
uv run ruff check src api tests docs scripts
uv run ruff format --check src api tests docs scripts
uv run bandit -q -r src
uv run vulture src --min-confidence 80

# make test
uv run python -m pytest

# make sphinx
uv run sphinx-build -W -b html docs docs/_build/html

# make distribution
uv build
```
`# make test-tps` / `# make test-notebook`  
Avec GNU Make et Bash disponibles, lancez `make test-tps` pour vérifier successivement l'exécution des notebooks, les tests Python, la construction du package et la documentation. La validation s'arrête au premier échec. Tous les notebooks du dossier `notebook/` sont exécutés, chacun sur une copie isolée avec une copie des modèles versionnés : les notebooks de prédiction utilisent les modèles du dépôt, et le notebook d'entraînement n'écrase pas ces derniers. Les sorties sont placées dans des répertoires temporaires, nettoyés même en cas d'échec. `make test-notebook` permet de vérifier uniquement les notebooks.

Pour les constructions autonomes, les sorties restent dans `dist/` et `docs/_build/html/`. Vous pouvez choisir d'autres répertoires avec `make distribution DIST_OUTPUT_DIR="chemin/dist"` et `make sphinx SPHINX_OUTPUT_DIR="chemin/html"`.
