summary: TP1 - Nettoyer le notebook
id: tp1
categories: tp
tags: tp
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP1 - Nettoyer le notebook

## Vue d'ensemble

Duration: 0:01:00

Pour réaliser ce TP, allez sur la branche `1_start_clean_notebook` depuis la racine du dépôt :
```shell
git stash --include-untracked
git checkout 1_start_clean_notebook
uv sync --locked
```

Dans le projet, vous trouverez :

```text
    .
    └── Formation-MLOps-1
        ├── input
        | ├── test.csv
        | ├── train.csv
        ├── notebook
        | ├── titanic.ipynb
        ├── pyproject.toml
        ├── uv.lock
        └── README.md
```

Voici l'état d'un prototype de science des données construit par l'un de vos collègues.

## Nettoyer le notebook

Duration: 0:20:00

Le but de cette première étape est de nettoyer le notebook en suivant les pratiques de code que vous venez de
découvrir :

- Choisissez des noms de variables explicites.
- Respectez les conventions de code.
- Respectez l'ordre des cellules.
- Limitez les affichages aux informations utiles.
- Supprimez le code inutile.
- Écrivez des fonctions courtes.
- Respectez l'immutabilité.
- Créez des fonctions pour les traitements réutilisables.

Pour vérifier que vous avez terminé, redémarrez le noyau du notebook et exécutez toutes les cellules dans l'ordre.

## Documenter les fonctions

Duration: 0:10:00

À ce stade, votre notebook est propre, il fonctionne et vous disposez de quelques fonctions.

Le but de cette étape est de documenter quelques fonctions.

Pour ce faire, utilisez des annotations de type et des docstrings.

Les annotations de type vous aideront à utiliser ces fonctions.

Les docstrings vous aideront à construire rapidement une bonne documentation dans les étapes suivantes.

## Extraire les fonctions dans un fichier .py

Duration: 0:10:00

À ce stade :

- Votre notebook est propre et fonctionne.
- Vous avez quelques fonctions documentées.

Le but de cette étape est d'extraire vos fonctions dans un fichier `.py`.

Vous pourrez ensuite réutiliser ces fonctions dans d'autres notebooks.

Pour ce faire :

- Créez un dossier `src` et un fichier vide `src/__init__.py`.
- Créez un fichier `feature_engineering.py` dans ce dossier.
- Déplacez le code de vos fonctions du notebook vers le fichier `.py`.
- Assurez-vous d'avoir tous les `import` nécessaires.
- Pour utiliser les fonctions dans le notebook, ajoutez :

```python
import sys

sys.path.append("../src/")
from feature_engineering import process_name
```

Cet exemple suppose que le répertoire de travail du notebook est `notebook/`. Importez explicitement les autres fonctions dont vous avez besoin. Nous passerons à l'import `src.feature_engineering` lors du packaging pour disposer d'un nom de module commun au notebook, aux tests et à l'API.

### Vérifier et formater le code avec Ruff

Depuis la racine du dépôt, vérifiez les fonctions extraites :

```sh
uv run ruff check src
uv run ruff format src
```

`ruff check` signale les problèmes de code, notamment les imports inutilisés. `ruff format` harmonise la mise en forme. Leur configuration se trouve dans `pyproject.toml`. Corrigez les problèmes signalés, puis relancez le notebook de bout en bout.

## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp2#0).
