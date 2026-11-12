summary: TP3 - Documenter avec Sphinx
id: tp3
categories: tp
tags: tp
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP3 - Documenter avec Sphinx

## Vue d'ensemble

Duration: 0:01:00

Pour réaliser ce TP, allez sur la branche `3_start_sphinx_doc` depuis la racine du dépôt :

```shell
git stash --include-untracked
git switch 3_start_sphinx_doc
uv sync --locked
```

Nouveautés sur cette branche :
- Des tests unitaires ont été rédigés.
- Le hook `.githooks/pre-commit` est en place. Si vous avez recloné le dépôt, réactivez-le avec `git config core.hooksPath .githooks`.
- Nouvelles commandes : `make test` (pytest), `make coverage` (tests avec mesure de la couverture, rapport dans `htmlcov/index.html`) et `make install-hooks` (active le hook).

L'objectif de ce TP est de créer une documentation HTML avec Sphinx à partir des docstrings. Deux parties optionnelles complètent le TP : un schéma d'architecture avec Mermaid, et une documentation d'architecture rédigée avec un agent de code.

## Initialiser la documentation

Duration: 0:05:00

Sphinx construit un site HTML à partir de fichiers texte et des docstrings du code. Son assistant, `sphinx-quickstart`, crée le dossier `docs` et sa configuration.

1. Depuis la racine du dépôt, lancez l'assistant :

```sh
uv run sphinx-quickstart docs
```

2. Répondez à ses questions comme ci-dessous, avec votre nom pour l'auteur. Répondez bien `n` à la première question : les chemins de ce TP supposent que les dossiers source et build ne sont pas séparés.

```text
> Separate source and build directories (y/n) [n]: n
> Project name: Titanic
> Author name(s): Votre nom
> Project release []: 0.1.0
> Project language [en]: fr
```

L'assistant crée notamment :
- `docs/conf.py` : la configuration de Sphinx ;
- `docs/index.rst` : la page d'accueil, avec sa table des matières (la directive `toctree`) ;
- `docs/_build/` : le dossier où le site sera construit.

Il crée aussi `docs/Makefile` et `docs/make.bat`, que ce TP n'utilise pas : Sphinx est lancé avec `uv run`.

Si l'assistant répond `Error: an existing conf.py has been found in the selected root path.`, le dossier `docs` existe déjà : supprimez-le avec `rm -rf docs`, puis relancez l'assistant.

## Configurer Sphinx pour lire le code

Duration: 0:05:00

Ouvrez `docs/conf.py`.

1. Tout en haut du fichier, ajoutez les lignes suivantes. Elles ajoutent la racine du dépôt, le dossier parent de `docs`, au chemin de recherche de Python : Sphinx peut alors importer le package `src`.

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

2. Remplacez la ligne `extensions = []` par :

```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]
```

L'extension `autodoc` lit les docstrings du code. L'extension `napoleon` met en forme les docstrings au format Google utilisées dans le projet, avec leurs sections `Args:` et `Returns:`.

## Générer la référence du code

Duration: 0:03:00

1. Générez une page par module de `src` :

```sh
uv run sphinx-apidoc -o docs/api src
```

La commande crée `docs/api/modules.rst` et `docs/api/src.rst`. Relancez-la quand vous ajoutez un module.

2. Ajoutez ces pages à la table des matières. Dans `docs/index.rst`, ajoutez la ligne `api/modules` à la fin de la directive `toctree`, indentée de trois espaces et précédée d'une ligne vide. La directive doit ressembler à ceci :

```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/modules
```

Sans la ligne vide, Sphinx prend `api/modules` pour une option : il signale `Error in "toctree" directive`, et la référence du code n'apparaît pas dans le site.

## Construire et vérifier la documentation

Duration: 0:05:00

1. Construisez le site :

```sh
uv run sphinx-build -b html docs docs/_build/html
```

La sortie doit se terminer par `build succeeded.` Lisez les lignes `WARNING` et `ERROR` qui s'affichent avant : elles sont expliquées plus bas.

2. Ouvrez le site dans votre navigateur : `open docs/_build/html/index.html` sous macOS, `start docs/_build/html/index.html` sous Windows (Git Bash), `xdg-open docs/_build/html/index.html` sous Linux.
3. Vérifiez le résultat : la page d'accueil liste `src`, et la page `src` présente les fonctions de `src/feature_engineering.py`, avec leurs paramètres sous le titre « Paramètres ».

En cas de problème :
- `WARNING: autodoc: failed to import`, suivi de `ModuleNotFoundError: No module named 'src'` : les lignes `sys.path` manquent en haut de `docs/conf.py`.
- `Error in "toctree" directive` : il manque la ligne vide avant `api/modules` dans `docs/index.rst`.
- Les docstrings affichent `Args:` tel quel, ou `ERROR: Unexpected indentation` : `sphinx.ext.napoleon` manque dans la liste `extensions`.
- Une modification n'apparaît pas : reconstruisez le site, en ajoutant `-E` à `sphinx-build` pour tout reconstruire.

La CI du TP4 construit la documentation avec l'option `-W`, qui transforme les avertissements en erreurs. Essayez-la : `uv run sphinx-build -W -b html docs docs/_build/html`.

## Aller plus loin : un thème et une page

Duration: 0:10:00

1. Changez de thème. Installez Furo, un thème moderne :

```sh
uv add --dev furo
```

Dans `docs/conf.py`, remplacez `html_theme = 'alabaster'` par `html_theme = 'furo'`, puis reconstruisez le site.

2. Ajoutez une page. Créez le fichier `docs/installation.rst` :

```rst
Installation
============

Depuis la racine du dépôt :

.. code-block:: sh

   uv sync
```

En reStructuredText, le trait sous un titre doit être au moins aussi long que le titre. Ajoutez `installation` à la directive `toctree` de `docs/index.rst`, sur sa propre ligne avant `api/modules`, puis reconstruisez le site.

Pour aller plus loin, la [documentation de Sphinx](https://www.sphinx-doc.org/fr/master/) existe en français.

## Optionnel : un schéma d'architecture avec Mermaid

Duration: 0:15:00

Mermaid décrit un schéma en texte, dans un fichier Markdown : il se versionne, se relit dans une pull request, et GitHub l'affiche directement. Ici, vous l'intégrez à la documentation Sphinx grâce à deux extensions : MyST, qui permet d'écrire des pages en Markdown, et `sphinxcontrib-mermaid`, qui dessine les schémas.

1. Installez les deux extensions comme dépendances de développement :

```sh
uv add --dev myst-parser sphinxcontrib-mermaid
```

2. Dans `docs/conf.py`, complétez la liste `extensions` et indiquez à MyST de traiter les blocs `mermaid` comme des schémas :

```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
    "sphinxcontrib.mermaid",
]
myst_fence_as_directive = ["mermaid"]
```

3. Créez le fichier `docs/architecture.md` avec le contenu ci-dessous. Les lignes `~~~` délimitent un bloc de code, comme trois accents graves.

```markdown
# Architecture

~~~mermaid
flowchart LR
    data["input/train.csv<br>input/test.csv"] --> fe["process_data<br>src/feature_engineering.py"]
    fe --> train["Random forest<br>notebook/titanic_train_model.ipynb"]
~~~
```

4. Ajoutez `architecture` à la directive `toctree` de `docs/index.rst`, sur sa propre ligne avant `api/modules`, puis reconstruisez la documentation et ouvrez la page Architecture. Le schéma est dessiné par le navigateur, qui charge Mermaid depuis Internet.
5. Complétez le schéma : que produit le notebook, et où ? (Indice : sa dernière cellule.) Pour un fichier de données, la forme en cylindre s'écrit `id[("texte")]`.

Pour essayer un schéma sans reconstruire la documentation, collez-le dans l'éditeur en ligne [mermaid.live](https://mermaid.live).

## Optionnel : faire rédiger la doc d'architecture par un agent de code

Duration: 0:15:00

Cette partie suppose qu'un agent de code est déjà installé dans votre VS Code : GitHub Copilot (chat en mode Agent), Claude Code ou opencode. Si ce n'est pas le cas, passez-la. Vérifiez aussi que votre entreprise autorise l'usage de cet outil sur votre code.

1. Ouvrez l'agent à la racine du dépôt et donnez-lui cette demande :

```text
Lis ce dépôt (src/, notebook/, tests/, Makefile, pyproject.toml) et rédige
docs/architecture.md, en français :
- le rôle de chaque dossier ;
- le chemin des données, des fichiers CSV jusqu'aux prédictions ;
- un schéma Mermaid de ce chemin ;
- pour chaque affirmation, le fichier ou la fonction qui la justifie.
N'invente rien et ne modifie aucun autre fichier. Si docs/architecture.md
existe déjà, complète-le sans supprimer le schéma.
```

2. Relisez le résultat comme une pull request : ouvrez chaque fichier cité et vérifiez ce qui est affirmé. Corrigez ce qui est faux, supprimez ce qui n'apporte rien.
3. Si vous avez fait la partie Mermaid, reconstruisez la documentation avec `-W` pour transformer les avertissements en erreurs : `uv run sphinx-build -W -b html docs docs/_build/html`. Sinon, ouvrez `docs/architecture.md` dans l'aperçu Markdown de VS Code (`Ctrl+Shift+V`, ou `Cmd+Shift+V` sur Mac).

L'agent écrit un brouillon : c'est vous qui en êtes responsable. Une doc d'architecture décrit l'état actuel du code et vieillit avec lui : gardez-la courte, pour pouvoir la tenir à jour.

## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp4#0).
