# 0001 : Le Makefile délègue toute logique sur plusieurs lignes à des scripts

- **Statut :** Accepté
- **Date :** 2026-11-10

## Contexte

Le Makefile est le point d'entrée unique des formateurs et des contributeurs (`make help`).
Il utilisait `.ONESHELL` pour écrire des recettes shell sur plusieurs lignes, par exemple pour exécuter le notebook dans un dossier temporaire.

Les formateurs et contributeurs utilisent des machines variées, et la version de `make` dépend de l'OS :

| Environnement | `make` par défaut |
|---|---|
| macOS (Command Line Tools de Xcode) | GNU Make 3.81 : Apple ne met plus l'outil à jour, les versions suivantes étant sous GPLv3 |
| Linux (distributions courantes), runners GitHub Actions | GNU Make 4.x |
| Windows | Aucun : à installer (Git Bash, Chocolatey…), version variable |

`.ONESHELL` n'existe qu'à partir de GNU Make 3.82. Avec une version antérieure, la directive est ignorée sans message : chaque ligne de recette s'exécute dans un shell séparé, et les variables ne passent pas d'une ligne à l'autre.
Une recette peut donc fonctionner chez un contributeur sous Linux et échouer chez un formateur sous macOS.
C'est ce qui est arrivé à `make test-tps`, qui échouait sur macOS avec `mkdir: /notebook: Read-only file system`. Une recette mal écrite peut même agir sur le mauvais dossier.

Les formateurs ont peu de temps pour se préparer. On ne peut pas leur demander d'installer une version particulière de `make`.
Sur les anciennes branches de TP, une logique shell dans le Makefile (`|| true` suivi de `status=$$?`) masquait aussi les échecs : le contrôle passait toujours.

## Décision

- **Toutes les règles passent par le Makefile.** C'est la seule interface à connaître.
- **Chaque recette tient sur une ligne logique.** Si elle a besoin de plusieurs commandes, elles sont chaînées avec `&&` et des `\` de continuation.
- **Dès qu'il faut de la logique** (variables partagées, nettoyage, conditions, analyse d'une sortie), elle va dans un **script Python** de `scripts/`, lancé avec `uv run python scripts/<script>.py`.
- Le Makefile vise la **plus ancienne version installée par défaut** sur les postes de l'équipe, aujourd'hui GNU Make 3.81 (macOS). Il n'utilise donc ni `.ONESHELL` ni `.SHELLFLAGS`, ni aucune autre fonctionnalité plus récente.
- Les scripts n'utilisent que la bibliothèque standard ou les dépendances déjà déclarées dans `pyproject.toml`. Ils renvoient un code de retour non nul en cas d'échec, et sont vérifiés par Ruff comme le reste du code (`PYTHON_DIRS`).

## Conséquences

- Le comportement est le même quelle que soit la version de `make` installée par défaut. Python est déjà requis par la formation, alors qu'imposer une version récente de `make` ajouterait un prérequis.
- Le Makefile reste lisible : une ligne par cible renvoie vers un script documenté.
- La logique est testable et vérifiée par le lint, ce qui n'est pas le cas d'un shell embarqué dans le Makefile.
- Les contributeurs doivent résister à la tentation d'ajouter du shell multi-lignes dans le Makefile. Un commentaire en tête du Makefile renvoie à cet ADR.
- Premier script concerné : `scripts/run_notebook.py` (exécution isolée d'un notebook, utilisée par `make test-notebook`).
