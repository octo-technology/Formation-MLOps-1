summary: TP2 - Écrire des tests unitaires
id: tp2
categories: setup
tags: setup
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP2 - Écrire des tests unitaires

## Vue d'ensemble

Duration: 0:01:00

Pour réaliser ce TP, allez sur la branche `2_start_unit_test` depuis la racine du dépôt :

```shell
git stash --include-untracked
git checkout 2_start_unit_test
uv sync --locked
```

Nouveautés sur cette branche :

- Le notebook est propre et exécutable de bout en bout.
- Quelques fonctions sont documentées.
- Les fonctions sont extraites dans un fichier .py spécifique.

L'objectif de ce TP est d'écrire quelques tests unitaires.

## Installer pytest
Duration: 0:05:00

Pour ajouter pytest comme dépendance de développement, utilisez :

```sh
uv add pytest --dev
```

Si pytest est déjà déclaré dans le groupe `dev` de `pyproject.toml`, la synchronisation de l'environnement l'a déjà installé.

## Écrire mon premier test unitaire

Duration: 0:10:00

Pour écrire des tests, nous allons :

- Utiliser le framework `pytest`.
- Utiliser le format "Given / When / Then".
- Suivre le paradigme "assert first".

1. Créez un dossier `tests` à la racine pour contenir l'ensemble des tests.
2. Créez un fichier `tests/test_feature_engineering.py`. En Python, nous suivrons ces conventions :
    - Préfixez les noms des fichiers de tests par `test_`.
    - Reprenez le nom du module contenant les fonctions à tester, après ce préfixe.
    - Commencez par un fichier de tests par module. Si ce fichier devient difficile à maintenir, examinez aussi les responsabilités du module testé.

Créez une fonction `test_process_name` selon le modèle suivant :

```python
def test_process_name():
    # Given

    # When

    # Then
    pass
```

Écrivez le `Then` en premier : nous allons nous assurer que le résultat est bien celui attendu en comparant deux DataFrames.

```python
import pandas as pd


def test_process_name():
    # Given

    # When

    # Then
    pd.testing.assert_frame_equal(expected_df, result_df)
```

Commencer par le `Then` permet de s'assurer que l'on sait ce que l'on veut valider. Cet extrait est volontairement incomplet : les variables seront définies dans les étapes suivantes.

Écrivez le `When` : l'appel à la fonction.

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

Finissez par écrire le `Given`.
  
```python
import pandas as pd
from src.feature_engineering import process_name


def test_process_name():
    # Given
    df = pd.DataFrame({"Name": ["Braund, Mr. Owen Harris"]})
    expected_df = pd.DataFrame(
        {
            "Name": ["Braund, Mr. Owen Harris"],
            "Name_Len": [23],
            "Name_Title": ["Mr."],
        }
    )

    # When
    result_df = process_name(df)

    # Then
    pd.testing.assert_frame_equal(expected_df, result_df)
```
Pour écrire les données de tests, nous recommandons (si ce ne sont pas des données personnelles ou confidentielles) d'utiliser des données de la production.

Depuis la racine du dépôt, exécutez les tests :

```sh
uv run python -m pytest
```

Vous pouvez aussi cliquer sur la flèche verte à côté du nom de la fonction dans PyCharm, en utilisant l'interpréteur de `.venv`.

## Écrire d'autres tests

Duration: 0:15:00

Pour vous exercer, écrivez trois autres tests automatisés sur d'autres fonctions.

## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp3#0).
