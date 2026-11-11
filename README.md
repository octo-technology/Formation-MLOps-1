# Formation MLOps 1 : Industrialisation de la Data Science

Un notebook Titanic écrit à la va-vite devient, TP après TP, du code propre, testé, documenté, vérifié par une CI, packagé, puis servi par une API dans un conteneur Docker.

## Les TP

Chaque TP commence sur sa propre branche, qui contient la solution des TP précédents.

| TP | Sujet | Branche de départ | Consignes |
|---|---|---|---|
| 0 | Installer l'environnement | `0_initial_state` | [TP 0](https://octo-technology.github.io/Formation-MLOps-1/tp0#0) |
| 1 | Nettoyer le notebook | `1_start_clean_notebook` | [TP 1](https://octo-technology.github.io/Formation-MLOps-1/tp1#0) |
| 2 | Écrire des tests unitaires | `2_start_unit_test` | [TP 2](https://octo-technology.github.io/Formation-MLOps-1/tp2#0) |
| 3 | Documenter avec Sphinx | `3_start_sphinx_doc` | [TP 3](https://octo-technology.github.io/Formation-MLOps-1/tp3#0) |
| 4 | Créer une CI GitHub | `4_start_ci` | [TP 4](https://octo-technology.github.io/Formation-MLOps-1/tp4#0) |
| 5 | Créer un package Python | `5_start_packaging` | [TP 5](https://octo-technology.github.io/Formation-MLOps-1/tp5#0) |
| 6 | Créer une API et la conteneuriser | `6_start_docker` | [TP 6](https://octo-technology.github.io/Formation-MLOps-1/tp6#0) |

La solution complète est sur la branche `final_state`.

## Quickstart

La formation utilise Python 3.15 (fixé dans `.python-version`), [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.13.5 pour l'environnement et Ruff pour le code. Depuis la racine du dépôt :

```sh
uv sync --locked      # crée .venv et installe les dépendances verrouillées
uv run jupyter lab    # ouvre JupyterLab
```

Pour passer à un TP, sauvegardez votre travail puis changez de branche :

```sh
git stash --include-untracked
git switch <branche-du-TP>
uv sync --locked
```

`make help` liste les commandes disponibles sur la branche.
