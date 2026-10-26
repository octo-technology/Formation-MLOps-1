summary: TP5 - Créer un package Python
id: tp5
categories: setup
tags: setup
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

Nouveauté sur cette branche :
- La CI est créée.

L'objectif de ce TP est de créer un package Python installable dans un autre projet.

## Créer un package Python

Duration: 0:05:00

Le fichier `pyproject.toml` contient déjà les métadonnées du projet et ses dépendances. Ajoutez-y le backend de construction et indiquez explicitement le package à distribuer :

```toml
[build-system]
requires = ["setuptools>=77.0.3"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
packages = ["src"]
```

Vérifiez que `src/__init__.py` existe. Ici, `src` est le nom du package importable, conservé pour correspondre aux imports des tests. Dans un nouveau projet, on choisirait généralement un nom plus spécifique.

Synchronisez l'environnement pour installer le projet en mode éditable, puis construisez les distributions :

```sh
uv sync
uv build
```

`uv sync` actualise aussi `uv.lock` après cette modification de configuration. `uv build` utilise le backend déclaré dans `pyproject.toml` pour produire une archive source et un wheel.

Vous pouvez constater le résultat dans le dossier `dist`, notamment `formation_mlops_1-0.1.0-py3-none-any.whl`.

Dans les notebooks, remplacez désormais les imports directs de `feature_engineering` et les modifications de `sys.path` par des imports depuis le package installé, par exemple `from src.feature_engineering import process_name`.

## Installer le package dans un autre projet

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
