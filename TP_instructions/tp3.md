summary: TP3 - Ajouter de la documentation avec Sphinx
id: tp3
categories: setup
tags: setup
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP3 - Ajouter de la documentation avec Sphinx

## Vue d'ensemble

Duration: 0:01:00

Pour réaliser ce TP, allez sur la branche `3_start_sphinx_doc` depuis la racine du dépôt :

```shell
git stash --include-untracked
git checkout 3_start_sphinx_doc
uv sync --locked
```

Nouveauté sur cette branche :
- Des tests unitaires ont été rédigés.

L'objectif de ce TP est de créer une documentation HTML avec Sphinx à partir des docstrings.

## Créer la documentation avec le formateur

Duration: 0:15:00

1. Vérifiez que les dépendances de développement sont installées : `uv sync --locked`.
2. Créez un dossier pour héberger la documentation : `mkdir ./docs`.
3. Allez dans ce dossier : `cd docs`.
4. Lancez l'assistant de Sphinx : `uv run sphinx-quickstart`.
5. Avec le formateur, complétez la configuration. Pour suivre les chemins ci-dessous, ne séparez pas les dossiers source et build.
6. Dans `conf.py`, ajoutez `sphinx.ext.autodoc` et `sphinx.ext.napoleon` à la liste `extensions`. Napoleon permet de traiter les docstrings au format Google utilisées dans le projet.
7. Rendez le code importable par Sphinx en ajoutant la racine du dépôt au début de `conf.py` :

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

Revenez à la racine du dépôt, puis générez les pages de référence des modules :

```sh
cd ..
uv run sphinx-apidoc -o docs/api src
```

Ajoutez `api/modules` dans la directive `toctree` de `docs/index.rst`, puis construisez la documentation :

```sh
uv run sphinx-build -b html docs docs/_build/html
```

Ouvrez `docs/_build/html/index.html` dans votre navigateur et vérifiez que les fonctions et leurs docstrings apparaissent.

## Explorer les possibilités de configuration

Duration: 0:15:00

En fonction du temps restant, explorez les possibilités offertes par [Sphinx](https://www.sphinx-doc.org/en/master/).


## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp4#0).
