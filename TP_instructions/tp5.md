summary: TP5 - Packager
id: tp5
categories: setup
tags: setup
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP5 - Packager

## Vue d'ensemble

Duration: 0:01:00

Pour réaliser ce TP, allez sur la branche `5_start_packaging`

```shell
git stash
git checkout 5_start_packaging
```

Nouveauté sur cette branche :
- La CI est créée.

L'objectif de ce TP est de créer un package python déployable.

## Créer un package python

Duration: 0:05:00

Pour créer un package python, il suffit de lancer la commande suivante :
```
uv build
```
La commande va se sourcer dans le pyproject.toml pour construire le package.

Vous pouvez constater le résultat dans le dossier `dist`.

## Installer le package. 

Créez vous un nouvel environnement virtuel et installez le package.
1. Initialisez le projet : `cd ..; uv init formation_test` dans votre terminal, en dehors du dossier de tp. Un dossier est créé à côté
2. Ajouter la dépendance : ` uv add ../Formation-MLOps-1/dist/formation_mlops_1-0.1.0-py3-none-any.whl`

NB : Ici, nous avons utilisé le .whl en local, en pratique, le whl serait sauvegardé dans un registre d'artefact puis serait téléchargé.
## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp6#0)