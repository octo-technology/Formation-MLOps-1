summary: TP5 - Créer un package Python
id: tp5
categories: tp
tags: tp
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP5 - Créer un package Python

## Vue d'ensemble

Duration: 0:01:00

Pour réaliser ce TP, allez sur la branche `5_start_packaging` depuis la racine du dépôt :

```shell
git stash --include-untracked
git checkout 5_start_packaging
uv sync --locked
```

Nouveautés sur cette branche :
- La CI est créée.
- Nouvelles commandes : `make static-validation` (Ruff, Bandit et Vulture, comme la CI) et `make dependency-scan` (Trivy).

L'objectif de ce TP est de créer un package Python installable dans un autre projet.

## Créer un package Python

Duration: 0:05:00

Le fichier `pyproject.toml` contient déjà les métadonnées du projet et ses dépendances. Ajoutez-y le backend de construction d'uv et indiquez le module à distribuer :

```toml
[build-system]
requires = ["uv_build>=0.13.5,<0.14.0"]
build-backend = "uv_build"

[tool.uv.build-backend]
module-name = "src"
module-root = ""
```

Par défaut, `uv_build` cherche un module nommé d'après le projet (`formation_mlops_1`) dans un dossier `src/`. Ici, le module s'appelle `src` et se trouve à la racine du dépôt : `module-name` donne son nom et `module-root = ""` indique qu'il est à la racine. Sans ces deux lignes, la construction échoue avec `Expected a Python module at: src/formation_mlops_1/__init__.py`. Toutes les options sont décrites dans la [documentation du backend d'uv](https://docs.astral.sh/uv/concepts/build-backend/#modules).

Vérifiez que `src/__init__.py` existe. Ici, `src` est le nom du package importable, conservé pour correspondre aux imports des tests. Dans un nouveau projet, on choisirait généralement un nom plus spécifique : `uv init --package` crée alors directement la structure attendue par défaut.

Synchronisez l'environnement pour installer le projet en mode éditable, puis construisez les distributions :

```sh
uv sync
uv build
```

`uv sync` actualise aussi `uv.lock` après cette modification de configuration. `uv build` utilise le backend déclaré dans `pyproject.toml` pour produire une archive source et un wheel.

Vous pouvez constater le résultat dans le dossier `dist`, notamment `formation_mlops_1-0.1.0-py3-none-any.whl`.

Dans les notebooks, supprimez désormais les `sys.path.append` : l'import `from src.feature_engineering import process_name` fonctionne grâce au package installé.

En mode éditable, vos modifications de `src` sont prises en compte sans réinstaller le package. Un noyau Jupyter déjà démarré garde toutefois les modules tels qu'ils étaient au moment de l'import : redémarrez-le, ou ajoutez en tête du notebook ces deux lignes, qui rechargent le code modifié avant chaque exécution de cellule :

```python
%load_ext autoreload
%autoreload 2
```

## Installer le package dans un autre projet

Duration: 0:10:00

Créez-vous un nouvel environnement virtuel et installez le package. Depuis la racine du dépôt :

```sh
cd ..
uv init --python 3.15 formation_test
cd formation_test
uv add ../Formation-MLOps-1/dist/formation_mlops_1-0.1.0-py3-none-any.whl
uv run python -c "import src.feature_engineering as feature_engineering; print(feature_engineering.__file__)"
```

Cette dernière commande vérifie que le module est importable depuis un projet indépendant. Le nom du wheel reflète le nom normalisé et la version déclarés dans `pyproject.toml` : adaptez le chemin si vous les modifiez.

NB : Ici, nous avons utilisé un wheel local. En pratique, il pourrait être publié dans un registre d'artefacts, puis téléchargé.

Revenez dans le dépôt de la formation avant de passer au TP suivant :

```sh
cd ../Formation-MLOps-1
```
## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp6#0).
