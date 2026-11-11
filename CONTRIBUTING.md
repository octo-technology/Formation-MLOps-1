# CONTRIBUTING

Quelques règles pour donner la formation et contribuer à ce repo.

Les contributeurs changent souvent et il n'y a pas de passation : tout ce qu'il faut savoir doit être écrit ici, dans le `README.md`, ou dans les décisions d'architecture de [`docs/adr/`](docs/adr/README.md).

- [CONTRIBUTING](#contributing)
  - [:mortar_board: Je donne la formation](#mortar_board-je-donne-la-formation)
  - [:bar_chart: Slides](#bar_chart-slides)
  - [:evergreen_tree: Organisation des branches](#evergreen_tree-organisation-des-branches)
  - [:card_index_dividers: Où modifier quoi](#card_index_dividers-où-modifier-quoi)
  - [:wrench: Pré-requis](#wrench-pré-requis)
  - [:speech_balloon: Proposer des améliorations](#speech_balloon-proposer-des-améliorations)
  - [:raising_hand: Prendre une tâche](#raising_hand-prendre-une-tâche)
    - [:computer: Quand ça touche au code](#computer-quand-ça-touche-au-code)
    - [:twisted_rightwards_arrows: Quand ça touche aux branches de TP](#twisted_rightwards_arrows-quand-ça-touche-aux-branches-de-tp)
    - [:page_with_curl: Quand ça touche aux slides](#page_with_curl-quand-ça-touche-aux-slides)
  - [:pencil2: Conventions de commit](#pencil2-conventions-de-commit)
  - [:straight_ruler: Règles de code](#straight_ruler-règles-de-code)
  - [:books: Documenter les décisions](#books-documenter-les-décisions)
  - [:black_joker: Référents](#black_joker-référents)

## :mortar_board: Je donne la formation

- Les apprenants clonent le dépôt : ils arrivent sur `0_initial_state`, la branche par défaut.
- Chaque TP indique sa branche de départ ; la solution complète est sur `final_state`.
- Avant une session, vérifie chaque branche : `git switch <branche> && uv sync --locked`, puis `make tpN-validation` (branches 1 à 6) ou `make test-tps` (`final_state`).
- Les consignes sont publiées sur GitHub Pages à chaque push sur `dev`. La version courante des slides est dans la section [Slides](#bar_chart-slides).

## :bar_chart: Slides

**Version courante : v1.13** :arrow_right: [Google Slides](https://docs.google.com/presentation/d/1Gqgs0yIp0Fq2Vr_496sL3EuBiLaXJQtVqciYcu2q7OQ/edit?usp=sharing)

## :evergreen_tree: Organisation des branches

- **`dev` est la source de vérité** : solution complète, consignes (`TP_instructions/`) et documentation formateur.
- **`N_start_X` est l'état de départ du TP N** : la solution des TP précédents, plus ce qu'il faut pour faire le TP N. `git diff <N> <N+1>` montre la correction du TP N.
- **`final_state`** : la solution complète, sans les fichiers réservés aux formateurs.
- **Branches** : `0_initial_state`, `1_start_clean_notebook`, `2_start_unit_test`, `3_start_sphinx_doc`, `4_start_ci`, `5_start_packaging`, `6_start_docker`, `final_state`.

## :card_index_dividers: Où modifier quoi

| Je veux modifier… | J'édite… |
|---|---|
| La solution finale (code, tests, API, Docker, CI) | les fichiers à la racine de `dev` |
| Le contenu d'une branche de TP | `dev`, puis chaque branche concernée : voir [Quand ça touche aux branches de TP](#twisted_rightwards_arrows-quand-ça-touche-aux-branches-de-tp) |
| Les consignes d'un TP | `TP_instructions/tpN.md` (publiées sur GitHub Pages à chaque push sur `dev`) |
| Une commande du `Makefile` | le `Makefile`. Une recette tient sur une ligne, toute logique plus complexe va dans `scripts/` ([ADR 0001](docs/adr/0001-scripts-pour-la-logique-du-makefile.md)) |
| Une dépendance | `uv add <paquet>` ou `uv add --group dev <paquet>`, puis commite `pyproject.toml` et `uv.lock` ensemble |
| Les slides | Google Slides, puis la section [Quand ça touche aux slides](#page_with_curl-quand-ça-touche-aux-slides) de ce fichier |

## :wrench: Pré-requis

- Avoir les droits d'écriture sur le [repo GitHub](https://github.com/octo-technology/Formation-MLOps-1) (sinon, travailler depuis un fork).
- Idéalement, avoir déjà suivi ou donné la formation pour les tâches qui touchent au support de slides.
- Avoir installé sur ta machine :
  - git ;
  - [uv](https://docs.astral.sh/uv/getting-started/installation/) ;
  - Python 3.15, fixé dans `.python-version` (uv le télécharge si besoin) ;

Pour les droits d'accès :arrow_right: contacte les [référents](#black_joker-référents) !

Pour vérifier ton installation :

```sh
uv sync --locked
make help
```

Puis installe le hook git qui lance `make static-validation` et `make test` avant chaque commit :

```sh
make install-hooks
```

## :speech_balloon: Proposer des améliorations

Passe par les [`issues` GitHub](https://github.com/octo-technology/Formation-MLOps-1/issues). Tu peux créer une `issue` pour :

- faire un retour sur la formation que tu as suivie ou donnée ;
- lancer une discussion :speech_balloon: ;
- proposer une amélioration du repo, du code des TP, des consignes ou du contenu des slides.

N'hésite pas à ajouter des détails ou des captures d'écran pour illustrer ton propos.

Si tu proposes une amélioration, explique le problème rencontré, propose une tâche et un moyen de la valider.

Si l'équipe de formateurs juge la demande pertinente et suffisamment détaillée, l'`issue` reste ouverte et peut être prise par n'importe quel contributeur.

## :raising_hand: Prendre une tâche

- Assigne-toi l'`issue` correspondante, pour que les autres sachent qu'elle est prise.
- Contacte les [référents](#black_joker-référents) si la tâche n'est pas assez claire pour toi ou si tu as un doute.

Avant toute modification, crée une branche depuis `dev` à jour :

```sh
git switch dev && git pull
git switch -c <type>/<description-courte>   # ex. fix/chemin-modeles, docs/guide-formateur
```

### :computer: Quand ça touche au code

1. Fais des commits petits et cohérents : **un commit = un changement logique**, avec un message qui respecte les [conventions de commit](#pencil2-conventions-de-commit).
2. Avant de pousser, vérifie que tout passe :
   ```sh
   make static-validation   # lint, mise en forme, sécurité et code mort (Ruff, Bandit, Vulture)
   make test                # tests unitaires
   make test-tps            # notebooks, tests, package et documentation
   ```
   `make test-tps` s'arrête au premier échec. Il exécute chaque notebook sur une copie isolée : les modèles versionnés ne sont pas modifiés et les sorties vont dans des dossiers temporaires.
3. Ouvre une Pull Request **vers `dev`** :
   - une PR traite **un seul sujet** ;
   - la description indique ce qui change, pourquoi, et comment tu l'as vérifié (les commandes lancées) ;
   - si la PR modifie le contenu d'un TP, précise lequel et vérifie que `TP_instructions/` reste cohérent ;
   - pour lier la PR à son `issue`, écris `Closes #<numéro>` dans la description : l'`issue` sera fermée automatiquement au merge.

Il n'y a pas de fichier de changelog : l'historique git, écrit avec les conventions de commit, en tient lieu (`git log --oneline`).

### :twisted_rightwards_arrows: Quand ça touche aux branches de TP

1. Modifie `dev` (PR vers `dev`).
2. Reporte le changement à la main dans chaque branche concernée, un commit par branche, par-dessus l'historique (jamais de force-push).
3. Sur chaque branche touchée, lance `make tpN-validation` (branches 1 à 6) ou `make test-tps` (`final_state`).

Règles des branches de TP :

- Le `Makefile` est cumulatif : chaque branche ajoute les cibles des commandes apprises au TP précédent.
- `make tpN-validation` vérifie l'état de départ du TP. Il tourne à chaque push dans `.github/workflows/tp-validation.yml`, uniquement sur ce dépôt (pas sur les forks des apprenants). `ci.yml` reste la CI de l'apprenant : sa solution du TP4 à partir de la branche 5.
- Le hook `.githooks/pre-commit` (à partir de la branche 3) est celui écrit au TP2.
- Les notebooks sont commités sans sorties, sauf le brouillon du TP1 (mauvaise pratique volontaire).
- Jamais de fichiers réservés aux formateurs : `TP_instructions/`, `docs/adr/`, `CONTRIBUTING.md`, `.github/workflows/static.yml`.

### :page_with_curl: Quand ça touche aux slides

Les slides sont sur Google Slides. La version à utiliser en formation est la **version courante** (section [Slides](#bar_chart-slides)).

Pour publier une nouvelle version :

1. Sur le Drive, duplique la version courante et renomme-la en incrémentant le numéro de version :
   - `1.13` :arrow_right: `1.14` pour des corrections ou de l'ajout de contenu ;
   - `1.13` :arrow_right: `2.0` pour une refonte (par exemple une nouvelle partie ou un nouveau déroulé) ;
   - contacte les [référents](#black_joker-référents) au besoin.
2. Fais tes modifications dans la copie.
3. Si le support est partagé aux participants, exporte-le en PDF et dépose-le sur le Drive.
4. Mets à jour ce fichier : la **version courante** et une nouvelle ligne en tête de l'**historique**, avec les liens et la liste des changements.
5. Ouvre une Pull Request. Si les slides et le code évoluent ensemble, mets-les à jour dans la même PR.

**Historique des versions**

| Version | Date | Google Slides | PDF | Changements |
|---|---|---|---|---|
| v1.13 | 2026 | [lien](https://docs.google.com/presentation/d/1Gqgs0yIp0Fq2Vr_496sL3EuBiLaXJQtVqciYcu2q7OQ/edit?usp=sharing) | — | Non documentés |
| v1.12 | 2026-04 | [lien](https://docs.google.com/presentation/d/1o92wKWZ14UpxlAIfIGWMEpIi95ceS325Ax8D52fXIds/edit?slide=id.g30d0616a363_0_3126#slide=id.g30d0616a363_0_3126) | — | Non documentés. Le code des branches de TP a été aligné sur cette version (passage à uv) |
| v1.5 | 2020-05-19 | [lien](https://docs.google.com/presentation/d/1Ps0Os2gzxhWqjDY-oC41yG36WAdv1mWSC8kk2UpXn5c/edit#slide=id.g804284dca3_0_176) | [lien](https://drive.google.com/file/d/1bmncpm9rFoFX0H3kRG7PSS0DI724c4IK/view) | Reformatage avec le template 2020-04 |
| v1.4 | 2020-05-18 | [lien](https://docs.google.com/presentation/d/1vcFUPkljpVcSD5P-XqLv0cB7iL_u7HXm8AKUidjqsKY/edit) | [lien](https://drive.google.com/file/d/1SVyVYvFhfyG0_Y0Ke2ZeloqTMExuUkoJ/view) | Ajout d'une section sur les règles à respecter pendant la formation |
| v1.3 | 2020-04-16 | [lien](https://docs.google.com/presentation/d/1pP-hnp8lXCprISyAaI7SSTbipMfG2J92y0c_LOTESgo/edit) | [lien](https://drive.google.com/file/d/1wlURivxbWbdMxD4FLyDNkhDR_cBXylMR/view) | Annexe sur les environnements conda et Docker, aide-mémoire d'installation sous Windows |

Les versions v1.6 à v1.11 n'ont pas été tracées.

## :pencil2: Conventions de commit

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

Si le titre ne suffit pas, ajoute un corps qui explique **pourquoi** le changement est nécessaire : le diff montre déjà le quoi.

## :straight_ruler: Règles de code

- Le code est vérifié par Ruff (lint et mise en forme), Bandit (sécurité) et Vulture (code mort) via `make static-validation`, avec les mêmes options que la CI. `make format` corrige la mise en forme. La configuration de Ruff se trouve dans `pyproject.toml`.
- Les noms (variables, fonctions, classes) sont en anglais. La documentation, les consignes, les messages de commit et les messages affichés aux utilisateurs sont en français.
- Tout nouveau dossier Python doit être ajouté à `PYTHON_DIRS` dans le `Makefile` et aux étapes Ruff de `.github/workflows/ci.yml` pour être vérifié par le lint.

## :books: Documenter les décisions

Une décision structurante (outil, organisation du repo, convention qui ne va pas de soi) fait l'objet d'un ADR dans [`docs/adr/`](docs/adr/README.md).
Avant de remettre en cause un choix existant, lis l'ADR correspondant. Pour changer de décision, écris un nouvel ADR qui remplace l'ancien.

## :black_joker: Référents

Le suivi des tâches passe par les `issues` GitHub. En cas de doute, ou pour obtenir des droits d'accès, contacte un référent :

- [toul@octo.com](https://askbob.octo.com/users/toul)
