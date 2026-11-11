summary: TP6 - Créer une API et la conteneuriser
id: tp6
categories: tp
tags: tp
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP6 - Créer une API et la conteneuriser

## Vue d'ensemble

Duration: 0:01:00

Pour réaliser ce TP, allez sur la branche `6_start_docker` depuis la racine du dépôt :

```shell
git stash --include-untracked
git switch 6_start_docker
uv sync --locked
```

Nouveautés sur cette branche :

- Le projet est packagé : `from src.feature_engineering import …` fonctionne sans `sys.path.append`.
- Un squelette de la classe `Preprocessor` est proposé dans `src/feature_engineering.py`, avec ses tests dans `tests/test_preprocessor.py`.
- Une API est mise à disposition dans `api/main.py`.
- Un `Dockerfile` à compléter est fourni.
- Nouvelle commande : `make distribution` (construit le package).

Au départ, le notebook `notebook/titanic_train_model.ipynb` échoue sur une erreur `TypeError … subscriptable` : c'est normal, la classe `Preprocessor` est à compléter.

L'objectif de ce TP est de conteneuriser une application de prédiction dans une image Docker.

## Découpler entraînement et inférence

Duration: 0:30:00

La première étape consiste à découpler la prédiction et l'entraînement.

Pour cela, il faut sauvegarder le modèle ainsi que les paramètres appris lors du prétraitement.

### Construire une classe de prétraitement

Pour sauvegarder les informations apprises lors du prétraitement, implémentez une classe `Preprocessor` qui possède deux méthodes inspirées de l'API scikit-learn : `fit_transform` et `transform`.

Un début d'implémentation est proposé dans `src/feature_engineering.py`. Complétez cette classe en y ajoutant les traitements nécessaires. Les paramètres sont appris dans `fit_transform`, puis réutilisés sans nouvel apprentissage dans `transform`.

Les tests de la classe sont fournis dans `tests/test_preprocessor.py`. Le test de `process_name` est commenté : décommentez-le une fois la méthode complétée, puis lancez `uv run python -m pytest`.

### Sauvegarder le modèle et le préprocesseur

Dans le notebook d'entraînement, importez `Preprocessor` depuis `src.feature_engineering`, instanciez-le sous le nom `processor`, puis entraînez le modèle sous le nom `rf`.

Avec `pickle`, sauvegardez les deux objets. Le notebook s'exécute depuis le dossier `notebook/` : le dossier `models` se trouve donc dans son dossier parent.

```python
import pickle
from pathlib import Path

MODELS_DIR = Path.cwd().parent / "models"
MODELS_DIR.mkdir(exist_ok=True)

with open(MODELS_DIR / "model_rf.pkl", "wb") as file_out:
    pickle.dump(rf, file_out)

with open(MODELS_DIR / "preprocessor.pkl", "wb") as file_out:
    pickle.dump(processor, file_out)
```

## Créer un notebook d'inférence

Duration: 0:10:00

Pour vérifier que l'entraînement et l'inférence sont bien découplés, créez un notebook `notebook/titanic_predict.ipynb`. Son répertoire de travail doit être `notebook/`.

Chargez les objets entraînés :

```python
import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.feature_engineering import Preprocessor

MODELS_DIR = Path.cwd().parent / "models"

with open(MODELS_DIR / "model_rf.pkl", "rb") as file_in:
    model: RandomForestClassifier = pickle.load(file_in)

with open(MODELS_DIR / "preprocessor.pkl", "rb") as file_in:
    preprocessor: Preprocessor = pickle.load(file_in)
```

Lisez le jeu de test, appliquez le prétraitement, puis exécutez l'inférence :

```python
test = pd.read_csv("../input/test.csv")
test_processed = preprocessor.transform(test)
predictions = model.predict_proba(test_processed)
```

Ce notebook doit fonctionner après un redémarrage du noyau, sans charger le jeu d'entraînement ni appeler `fit_transform`.

## Découvrir l'API

Duration: 0:10:00

Maintenant que l'entraînement et l'inférence sont découplés, nous pouvons faire nos prédictions via une API.

Dans le fichier `api/main.py`, une API écrite avec FastAPI permet de faire des prédictions.

Depuis la racine du dépôt, lancez-la localement avec la commande suivante, après avoir sauvegardé les objets entraînés :

```shell
uv run uvicorn api.main:app
```

Puis, dans votre navigateur, consultez l'URL : `http://127.0.0.1:8000/predict/3/Braund,%20Mr.%20Owen%20Harris/male/?age=23`.

La route reçoit la classe du passager, son nom et son sexe dans le chemin. L'âge est un paramètre de requête. Explorez `api/main.py` et la [documentation interactive](http://127.0.0.1:8000/docs) pour découvrir les autres paramètres.

## Tester l'API (Lecture)

Duration: 0:10:00

Voici comment tester l'API, au format « Given / When / Then » vu au TP2.

FastAPI fournit un client de test, `TestClient`, qui appelle l'API sans lancer de serveur. À l'import de `api.main`, l'API charge les objets entraînés : ils doivent avoir été sauvegardés.

- `Then` : la réponse réussit (code HTTP 200) et contient deux probabilités dont la somme vaut 1. Les valeurs exactes dépendent du modèle entraîné : le test ne vérifie pas leur valeur.
- `When` : un appel `GET` sur la route de prédiction avec `client.get(test_url)`.
- `Given` : le client de test et l'URL d'un passager, celle utilisée plus haut.

Copiez ce test dans `tests/test_api.py` :

```python
import pytest
from fastapi.testclient import TestClient

from api.main import app


def test_predict_should_return_probabilities():
    # Given
    client = TestClient(app)
    test_url = "/predict/3/Braund,%20Mr.%20Owen%20Harris/male/?age=23"

    # When
    response = client.get(test_url)

    # Then
    assert response.status_code == 200
    probabilities = response.json()["input_proba"]
    assert len(probabilities) == 2
    assert sum(probabilities) == pytest.approx(1)
```

Depuis la racine du dépôt, lancez les tests :

```sh
uv run python -m pytest
```

## Conteneuriser le tout

Duration: 0:20:00

Nous souhaitons maintenant faire tourner cela dans une image Docker pour assurer une reproductibilité en production.

Commencez par installer Docker sur votre machine et démarrez son moteur.

Découvrez et complétez le `Dockerfile` : installez uv dans l'image, copiez les fichiers du projet, synchronisez les dépendances avec `uv sync --locked --no-dev`, puis lancez Uvicorn depuis l'environnement `.venv`. Le serveur doit écouter sur `0.0.0.0`, au port 80.

Depuis la racine du dépôt, construisez l'image et lancez le conteneur :

```shell
docker build -t mlops-1 .
docker run --rm -p 8080:80 mlops-1
```

Le port 80 du conteneur est exposé sur le port 8080 de votre machine. La documentation Swagger est disponible [ici](http://127.0.0.1:8080/docs) et permet d'interagir avec l'API.

Vous pouvez aussi consulter la [route de prédiction d'exemple](http://127.0.0.1:8080/predict/3/Braund,%20Mr.%20Owen%20Harris/male/?age=23).

## Fin

Duration: 0:01:00

C'était le dernier TP de cette formation, merci de l'avoir suivie avec nous.
