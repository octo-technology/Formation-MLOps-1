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

Pour réaliser ce TP, allez sur la branche `6_start_docker`

```shell
git stash
git checkout 6_start_docker
```

Nouveauté sur cette branche :

- Le fichier `setup.py` est créé.
- Une API est mise à disposition

L'objectif de ce TP est de créer une application avec une image docker.

## Découpler entraînement et inférence

Duration: 0:30:00

La première étape pour réussir à faire une application qui permet de faire des predictions est de réussir à découpler
prédiction et entraînement.

Pour cela, il nous faut sauvegarder le modèle et aussi tous les objets appris au moment du préprocessing.

### Construire une classe de pré-processing

Pour sauvegarder les informations apprises au moment du pré-processing, nous proposons d'implémenter une
classe `Preprocessor`
qui a deux méthodes inspirées de l'API `scikit-learn` : `fit_transform` et `transform`.

Nous avons proposé un début d'implémentation dans `src.feature_engineering` à vous de compléter cette classe en y
ajoutant toutes les méthodes.

### Sauvegarder le modèle et le pré-processor

Avec `pickle` sauvegarder les deux objets :

```python
with open("./models/model_rf.pkl", "wb") as file_out:
    file_out.dump(model)

with open("./models/preprocessor.pkl", "rb") as file_out:
    file_out.dump(preprocessor)
```

## Créer un notebook d'inférence

Duration: 0:10:00

Pour vérifier que l'on a bien découplé `train` et `predict` créer un notebook `inference.pkl`

Chargez les objets entraînés :

```python

with open("./models/model_rf.pkl", "rb") as file_in:
    model: RandomForestClassifier = pickle.load(file_in)

with open("./models/preprocessor.pkl", "rb") as file_in:
    preprocessor: Preprocessor = pickle.load(file_in)
```

Lire le jeu de test par exemple

```python
import pandas as pd

pd.read_csv("data/test.csv")
```

Puis exécuter le préprocessing, ensuite l'inférence

## Découvrir l'API

Duration: 0:10:00

Maintenant que l'on a bien découplé `train` et `predict` nous pouvons faire nos prédictions via une api.

Dans le fichier `api/main.py` nous proposons une api écrite avec fastapi qui permet de faire des prédictions.

Vous pouvez la lancer localement avec la commande :

```shell
uvicorn api.main:app
```

Puis dans votre navigateur requetez l'url : `http://127.0.0.1:8000/predict/0/Braund,%20Mr.%20Owen%20Harris/23/`

Explorez le fichier `api/main.py` pour comprendre comment cela marche

## Conteneuriser le tout

Duration: 0:20:00

Nous souhaitons maintenant faire tourner cela dans une image Docker pour assurer une reproductibilité en production.

Commencez par installer Docker sur votre machine.

Puis découvrir et compléter le `Dockerfile`

Pour lancer le docker :

```shell
docker build -t mlops-1 .
docker run -p 80:80 mlops-1
```

L'API est exposée et peut être atteinte à 0.0.0.0:80 La documentation est disponible [ici](http://127.0.0.1/docs),
générée par swagger, elle peut également être utilisée pour interagir avec l'API.

Sinon, vous pouvez faire appel à la même route d'exemple.

## Fin

Duration: 0:01:00

C'était le dernier TP de cette formation, merci de l'avoir suivie avec nous.