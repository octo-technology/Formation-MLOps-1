# Contribuer à la formation MLOps 1

Ce guide décrit comment le dépôt est organisé et comment y contribuer.
Les contributeurs changent souvent : tout ce qu'il faut savoir doit être écrit ici, dans le `README.md`, ou dans les décisions d'architecture de [`docs/adr/`](docs/adr/README.md).

## `dev` est la source de vérité

- **`dev`** contient la solution complète de la formation (code final, notebooks, documentation, CI, Docker) ainsi que les consignes des TP (`TP_instructions/`).
- **Les branches de TP** (`0_initial_state`, `1_start_clean_notebook`, …) contiennent l'état de départ de chaque TP pour les apprenants. Elles sont dérivées de `dev`.
- **On ne commite jamais directement sur une branche de TP.** Toute modification se fait sur `dev`, puis les branches de TP sont mises à jour à partir de `dev`.

## Déroulé d'une contribution

1. Partir de `dev` à jour et créer une branche de travail :
   ```sh
   git switch dev && git pull
   git switch -c <type>/<description-courte>   # ex. fix/chemin-modeles, docs/guide-formateur
   ```
2. Faire des commits petits et cohérents : **un commit = un changement logique**.
3. Avant de pousser, vérifier que tout passe :
   ```sh
   make static-validation   # lint et mise en forme (Ruff)
   make test                # tests unitaires
   make test-tps            # notebook, tests, package et documentation
   ```
4. Ouvrir une Pull Request **vers `dev`**.

## Conventions de commit

Les messages suivent [Conventional Commits](https://www.conventionalcommits.org/fr/), avec une description **en français** :

```text
<type>(<scope optionnel>): <description à l'infinitif, sans majuscule ni point final>
```

| Type | Usage | Exemple |
|---|---|---|
| `feat` | nouvelle fonctionnalité | `feat(make): ajouter la cible install-hooks` |
| `fix` | correction de bug | `fix(api): charger les modèles indépendamment du dossier courant` |
| `docs` | documentation uniquement | `docs: ajouter le guide de contribution` |
| `refactor` | restructuration sans changement de comportement | `refactor(notebook): renommer les notebooks` |
| `test` | ajout ou correction de tests | `test: couvrir le cas sans tarif` |
| `ci` | intégration continue | `ci: vérifier la génération des branches de TP` |
| `chore` | maintenance (dépendances, configuration, `.gitignore`…) | `chore(deps): mettre à jour scikit-learn` |

Scopes courants : `make`, `api`, `notebook`, `src`, `tests`, `docs`, `tp`, `deps`.

## Pull Requests

- Une PR traite **un seul sujet**.
- La description indique ce qui change, pourquoi, et comment ça a été vérifié (les commandes lancées).
- Si la PR modifie le contenu d'un TP, préciser lequel et vérifier que `TP_instructions/` reste cohérent.

## Où modifier quoi

| Je veux modifier… | J'édite… |
|---|---|
| La solution finale (code, tests, API, Docker, CI) | les fichiers à la racine de `dev` |
| Les consignes d'un TP | `TP_instructions/tpN.md` (publiées sur GitHub Pages à chaque push sur `dev`) |
| Une commande du `Makefile` | le `Makefile`. Une recette tient sur une ligne, toute logique plus complexe va dans `scripts/` ([ADR 0001](docs/adr/0001-scripts-pour-la-logique-du-makefile.md)) |
| Une dépendance | `uv add <paquet>` ou `uv add --group dev <paquet>`, puis commiter `pyproject.toml` et `uv.lock` ensemble |

## Règles de code

- Le code est vérifié et mis en forme par Ruff (`make static-validation`, `make format`). La configuration se trouve dans `pyproject.toml`.
- Les noms (variables, fonctions, classes) sont en anglais. La documentation, les consignes, les messages de commit et les messages affichés aux utilisateurs sont en français.
- Tout nouveau dossier Python doit être ajouté à `PYTHON_DIRS` dans le `Makefile` et aux étapes Ruff de `.github/workflows/ci.yml` pour être vérifié par le lint.

## Documenter les décisions

Une décision structurante (outil, organisation du dépôt, convention qui ne va pas de soi) fait l'objet d'un ADR dans [`docs/adr/`](docs/adr/README.md).
Avant de remettre en cause un choix existant, lisez l'ADR correspondant. Pour changer de décision, écrivez un nouvel ADR qui remplace l'ancien.
