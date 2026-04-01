summary: TP2 - Unit testing
id: tp2
categories: setup
tags: setup
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP2 - Unit testing

## Vue d'ensemble

Duration: 0:01:00

Pour réaliser ce TP, allez sur la branche `2_start_unit_test`

```shell
git stash
git checkout 2_start_unit_test
```

Nouveauté sur cette branche :

- Le notebook est propre et est exécutable de bout en bout
- Quelques fonctions sont documentées.
- Les fonctions sont extraites dans un fichier .py spécifique.

L'objectif de ce TP est d'écrire quelques tests unitaires.

## Installer pytest 
Duration: 0:05:00

```
uv add pytest --dev
```

## Écrire mon premier test unitaire

Duration: 0:10:00

Pour écrire des tests, nous allons :

- Utiliser le framework `pytest`.
- Utiliser le format "Given / When / Then".
- Suivre le paradigme "assert first".

1. Créer un dossier `tests` à la racine qui va contenir l'ensemble des tests
2. Créer un fichier `test_feature_engineering.py`. En python la convention veut que les fichiers de tests :
    - Soient préfixés par `test_`.
    - Aient le même nom que le fichier contenant les fonctions à tester.
    - 1 fichier de fonctions implique donc un fichier de test. Si vous ressentez le besoin de découper en plusieurs
      fichiers de tests, c'est probablement qu'il faut découper le fichier contenant les fonctions également.

Créer une fonction `test_process_name` selon le template suivant :

```python
def test_process_name():
   # Given
 
   # When
 
   # Then
 ```

Écrire le `then` en premier, nous allons nous assurer que le résultat est bien celui attendu, en comparant 2 data
   frames.

```python
import pandas as pd
    
def test_process_name():
   # Given
 
   # When
 
   # Then
   pd.testing.assert_frame_equal(expected_df, result_df)
 ```

Commencez par le Then permet de s'assurer que l'on sait ce que l'on veut valider

Écrire le `when` : l'appel à la fonction

```python
import pandas as pd
from src.feature_engineering import process_name
    
def test_process_name():
   # Given
 
   # When
   result_df = process_name(df)
    
   # Then
   pd.testing.assert_frame_equal(expected_df, result_df)
 ```

Finir par écrire le `given`
  
```python
import pandas as pd
from src.feature_engineering import process_name
    
def test_process_name():
   # Given
   df = pd.DataFrame({"Name": ["Braund, Mr. Owen Harris"]})
   expected_df = pd.DataFrame({"Name": ["Braund, Mr. Owen Harris"],
                               "Name_Len": [23],
                               "Name_Title": "Mr."})
   # When
   result_df = process_name(df)
    
   # Then
   pd.testing.assert_frame_equal(expected_df, result_df)
```
Pour écrire les données de tests, nous recommandons (si ce ne sont pas des données personnelles ou confidentielles) d'utiliser des données de la production.

Exécuter les tests en cliquant sur la petite flèche verte à côté du nom de la fonction ou lancer la commande `uv run pytest` ou `pytest`

## Écrire d'autres tests

Duration: 0:15:00

Pour vous exercer, écrivez 3 autres tests automatisés sur d'autres fonctions.

## Ajouter du linting

Duration: 0:10:00

Les tests c'est bien, mais autant s'assurer aussi que le code est propre **avant** de le tester. C'est le rôle du linting : vérifier automatiquement le style et les erreurs courantes.

On va utiliser `ruff`, un linter Python ultra-rapide, déjà configuré dans le `pyproject.toml`.

1. Installer ruff en dépendance de développement :

```shell
uv add ruff --dev
```

2. Lancer le linting :

```shell
uv run ruff check src tests
```

Si tout va bien, aucune sortie. Sinon, ruff vous indique les lignes à corriger.

3. Pour corriger automatiquement ce qui peut l'être :

```shell
uv run ruff check src tests --fix
```

Jetez un œil à la section `[tool.ruff]` dans `pyproject.toml` pour voir les règles activées. On y retrouve entre autres les vérifications de style (pycodestyle), les imports (isort), et les bugs courants (flake8-bugbear).

## Le Makefile, votre couteau suisse

Duration: 0:05:00

Plutôt que de retenir toutes les commandes `uv run ...`, un `Makefile` à la racine du projet centralise les tâches courantes. Pour voir les commandes disponibles :

```shell
make help
```

Quelques exemples :

- `make install` — installe les dépendances
- `make lint` — lance le linting (ruff, bandit, vulture)
- `make test` — lance les tests unitaires
- `make sphinx` — génère la documentation
- `make distribution` — construit le package

L'avantage : tout le monde utilise les mêmes commandes, et la CI peut aussi s'appuyer dessus. Pas besoin de se souvenir des options de chaque outil.

## Automatiser avec un pre-commit hook

Duration: 0:10:00

C'est bien de lancer le linting et les tests à la main, mais on oublie vite. L'idée du **pre-commit hook**, c'est de les lancer **automatiquement** à chaque `git commit`. Si ça échoue, le commit est bloqué — impossible de pousser du code qui ne passe pas les vérifications.

1. Créer le dossier `.githooks` à la racine du projet et y ajouter un fichier `pre-commit` :

```bash
mkdir -p .githooks
```

```bash
# .githooks/pre-commit
#!/bin/bash
set -e

echo "🔍 Running lint..."
make lint

echo "🧪 Running tests..."
make test

echo "✅ All checks passed!"
```

2. Rendre le script exécutable et configurer git pour utiliser ce dossier de hooks :

```shell
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

Ou plus simplement, si la target existe dans le Makefile :

```shell
make install-hooks
```

3. Testez ! Faites un changement quelconque et tentez un `git commit`. Vous devriez voir le lint et les tests se lancer automatiquement. Si l'un des deux échoue, le commit sera refusé.

> **Astuce** : en cas d'urgence, vous pouvez contourner le hook avec `git commit --no-verify`, mais c'est à utiliser avec parcimonie 😉

## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp3#0)
