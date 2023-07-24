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

## Écrire mon premier test unitaire

Duration: 0:10:00

Pour écrire des tests, nous allons utiliser le framework `pytest`.

1. Créer un dossier `tests` à la racine qui va contenir l'ensemble des tests
2. Créer un fichier `test_feature_engineering.py`. En python la convention veut que les fichiers de tests :
    - Soient préfixés par `test_`.
    - Aient le même nom que le fichier contenant les fonctions à tester.
    - 1 fichier de fonctions implique donc un fichier de test. Si vous ressentez le besoin de découper en plusieurs
      fichiers de tests, c'est probablement qu'il faut découper le fichier contenant les fonctions également.

3. Pour écrire les tests, nous recommandons d'utiliser le format "Given / When / Then" et le paradigme "assert first"
    1. Créer une fonction `test_process_name` selon le template suivant:
       ```python
       def test_process_name():
          # Given
    
          # When
    
          # Then
        ```
    2. Écrire le `then` en premier, nous allons nous assurer que le résultat est bien celui attendu, en comparant 2 data
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
    3. Écrire le `when` : l'appel à la fonction
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
    4. Finir par écrire le `given`
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
       Pour écrire les données de tests, nous recommandons (si ce ne sont pas des données personnelles ou
       confidentielles) d'utiliser des données de la production.
4. Exécuter les tests en cliquant sur la petite flèche verte à côté du nom de la fonction

## Écrire d'autres tests

Duration: 0:15:00

Pour vous exercer, écrivez 3 autres tests automatisés sur d'autres fonctions.


## Lien vers le TP suivant

Duration: 0:01:00

Les instructions du TP suivant sont [ici](https://octo-technology.github.io/Formation-MLOps-1/tp3#0)