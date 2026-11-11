summary: TP0 - Préparation de l'environnement de travail
id: tp0
categories: setup
tags: setup
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP0 - Préparation de l'environnement de travail

## Vue d'ensemble

Duration: 0:01:00

L'objectif de ce TP est de préparer votre environnement de travail pour pouvoir développer efficacement un projet de science des données.

Tel l'artisan, le _craftsman_ Data Scientist doit maîtriser ses outils.

## Récupérer le projet sur GitHub

Duration: 0:03:00

Clonez le dépôt avec la commande suivante :

```sh
git clone git@github.com:octo-technology/Formation-MLOps-1.git
```

NB : Sous Windows, installez [Git for Windows](https://gitforwindows.org/) pour disposer de Git et de Git Bash.

Le clonage via SSH nécessite une clé associée à votre compte GitHub. Vous pouvez aussi cloner le dépôt via HTTPS :

```sh
git clone https://github.com/octo-technology/Formation-MLOps-1.git
```


## Ouvrir le projet dans votre éditeur

Duration: 0:03:00

La formation peut se suivre avec PyCharm ou VS Code. Ouvrez le dossier du projet dans l'un des deux.

Avec VS Code, installez les extensions Python et Jupyter de Microsoft.

Sous Windows, configurez le terminal de l'éditeur pour utiliser Git Bash et suivre les commandes shell de cette formation :

- PyCharm : dans Paramètres > Outils > Terminal, remplacez le chemin du shell par celui de Git Bash, généralement `"C:\Program Files\Git\bin\bash.exe" --login -i`.
- VS Code : ouvrez la palette de commandes (`Ctrl+Shift+P`), lancez « Terminal: Select Default Profile » et choisissez Git Bash.

Ouvrez un nouveau terminal et vérifiez l'installation avec `git --version`.

## Créer un environnement avec uv

Duration: 0:10:00

### Installer uv

Source : [documentation d'installation de uv](https://docs.astral.sh/uv/getting-started/installation/).

Sur Linux ou macOS :
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ou, si pipx est déjà installé :
```sh
pipx install uv
```

Sous Windows, exécutez cette commande dans PowerShell :
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Après l'installation, ouvrez un nouveau terminal dans votre éditeur et vérifiez que `uv --version` fonctionne.

### Installer l'environnement et les dépendances

Le projet utilise Python 3.15, fixé dans le fichier `.python-version` (créé avec `uv python pin 3.15`). Si cette version n'est pas installée sur votre machine, uv la télécharge automatiquement.

Depuis la racine du dépôt (`cd Formation-MLOps-1`), créez l'environnement `.venv` et installez les dépendances déclarées dans `pyproject.toml`, aux versions de `uv.lock` :

```sh
uv sync --locked
```

Sélectionnez ensuite l'interpréteur de ce nouvel environnement, `.venv/bin/python` sous Linux ou macOS, ou `.venv\Scripts\python.exe` sous Windows :

- PyCharm : dans Paramètres > Projet > Interpréteur Python, ajoutez un interpréteur existant.
- VS Code : ouvrez la palette de commandes et lancez « Python: Select Interpreter ». Dans un notebook, choisissez le même environnement comme noyau (« Select Kernel »).

Toutes les commandes Python de la formation seront lancées avec `uv run`, qui utilise cet environnement sans nécessiter son activation manuelle.

NB : Pour installer uniquement les dépendances de production, utilisez `uv sync --locked --no-dev`.


## Ouvrir un notebook
Duration: 0:03:00

Depuis la racine du dépôt, lancez JupyterLab :

```sh
uv run jupyter lab
```

## Comment suivre ces TP

Duration: 0:03:00

Les TP sont étroitement liés à la présentation de la formation.

Chaque TP commence sur une branche dédiée. Pour consulter l'état initial :

```sh
git switch 0_initial_state
```

Pour naviguer entre les étapes, suivez les changements de branche indiqués au début de chaque TP, puis exécutez `uv sync --locked` pour synchroniser l'environnement.

Avant chaque changement de branche, `git stash --include-untracked` sauvegarde les modifications et les nouveaux fichiers de votre exercice. Vous pouvez retrouver ces sauvegardes avec `git stash list`.

Pour voir toutes les branches :
```sh
git branch -a
```
## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp1#0).
