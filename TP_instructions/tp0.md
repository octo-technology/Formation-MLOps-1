summary: TP0 - Setup de l'environnement de travail
id: tp0
categories: setup
tags: setup
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP0 - Préparation de l'environnement de travail

## Vue d'ensemble

Duration: 0:01:00

L'objectif de ce TP est de setup votre environnement de travail pour pouvoir développer efficacement un projet de DS.

Tel l'artisan, le _craftsman_ Data Scientist doit maitriser ses outils

## Récupérer le projet sur GitHub

Duration: 0:03:00

Cloner le repository avec la commande suivante : 

```sh
git clone git@github.com:octo-technology/Formation-MLOps-1.git
```

NB : Si vous êtes sur Windows, vous aurez besoin de l'utilitaire [Git for windows](https://gitforwindows.org/)

## Ouvrir pycharm et le configurer

Duration: 0:03:00

Ouvrir le projet sur PyCharm

### Installer uv
Source : https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1

Sur ubuntu / mac : 
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

ou
```
pipx install uv
```

Sur windows 
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installer la bonne version de Python

```sh
uv python install 3.14
```

Assurez vous que la version de Python 3.14 est bien la dernière (>= 3.14.0). 
```sh
uv run python --version
```

Si ce n'est pas le cas (version du type `Python 3.14.0b2`), assurez vous qu'uv est à jour en relancer le script d'installation puis vous pouvez relancer `uv python install 3.14` qui devrait alors donner une version stable.


### Installer l'environnement uv et les packages
Positionnez-vous dans le dossier de la formation

```sh
cd Formation-MLOps-1
```

Créer un environnement uv et installer toutes les dépendances avec 

```sh
uv sync
```

NB : Si vous êtes dans un environnement de production, et ne souhaitez pas installer les dépendances de dev, il convient d'utiliser la commande `uv sync --no-dev`


## Ouvrir un notebook
Duration: 0:03:00

Dans le terminal taper la commande : 

```sh
uv run --with jupyter jupyter lab
```

Si l'environnement `formation_mlops_1` n'est pas disponible dans l'interface `jupyter` :

- Quittez jupyter-notebook avec un <kbd>ctrl</kbd>+<kbd>c</kbd> dans le terminal
- Lancer `ipython kernel install --name "PythonIndus" --user`
- Relancer `jupyter-notebook`

## Comment suivre ce TP

Duration: 0:03:00

Il est fortement lié à la présentation de la formation.

Pour naviguer entre les étapes, changez de branche.

Pour voir toutes les branches
```sh
git branch -a
```
## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp1#0)
