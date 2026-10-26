summary: TP6 - Conteneuriser
id: tp6
categories: setup
tags: setup
status: Published
authors: OCTO Technology
Feedback Link: https://github.com/octo-technology/Formation-MLOps-1/issues/new/choose

# TP6 - Conteneuriser

## Vue d'ensemble

Duration: 0:01:00

Pour réaliser ce TP, allez sur la branche `6_start_docker` depuis la racine du dépôt :

```shell
git stash --include-untracked
git checkout 6_start_docker
uv sync --locked
```

Nouveauté sur cette branche :

- Une API est mise à disposition.

L'objectif de ce TP est de conteneuriser une application de prédiction dans une image Docker.

## Découpler entraînement et inférence

Duration: 0:30:00

La première étape consiste à découpler la prédiction et l'entraînement.

Pour cela, il faut sauvegarder le modèle ainsi que les paramètres appris lors du prétraitement.

### Construire une classe de prétraitement

Pour sauvegarder les informations apprises lors du prétraitement, implémentez une classe `Preprocessor` qui possède deux méthodes inspirées de l'API scikit-learn : `fit_transform` et `transform`.

Un début d'implémentation est proposé dans `src/feature_engineering.py`. Complétez cette classe en y ajoutant les traitements nécessaires. Les paramètres sont appris dans `fit_transform`, puis réutilisés sans nouvel apprentissage dans `transform`.

### Sauvegarder le modèle et le préprocesseur

Dans le notebook d'entraînement, importez `Preprocessor` depuis `src.feature_engineering`, instanciez-le sous le nom `preprocessor`, puis entraînez le modèle sous le nom `model`.

Avec `pickle`, sauvegardez les deux objets. Les chemins suivants supposent que le répertoire de travail du notebook est `notebook/` :

```python
import pickle
from pathlib import Path

Path("../models").mkdir(exist_ok=True)

with open("../models/model_rf.pkl", "wb") as file_out:
    pickle.dump(model, file_out)

with open("../models/preprocessor.pkl", "wb") as file_out:
    pickle.dump(preprocessor, file_out)
```

## Créer un notebook d'inférence

Duration: 0:10:00

Pour vérifier que l'entraînement et l'inférence sont bien découplés, créez un notebook `notebook/inference.ipynb`. Son répertoire de travail doit être `notebook/`.

Chargez les objets entraînés :

```python
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.feature_engineering import Preprocessor

with open("../models/model_rf.pkl", "rb") as file_in:
    model: RandomForestClassifier = pickle.load(file_in)

with open("../models/preprocessor.pkl", "rb") as file_in:
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
