from typing import Optional

from fastapi import FastAPI
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble._forest import RandomForestClassifier
from indus.feature_engineering import MainTransformer

app = FastAPI()

with open("./models/model_rf.pkl", "rb") as file_in:
    model: RandomForestClassifier = pickle.load(file_in)

with open("./models/transformer.pkl", "rb") as file_in:
    transformer: MainTransformer = pickle.load(file_in)


@app.get("/predict/{pclass}/{name}/{sex}/")
async def predict(
    pclass: int,
    name: str,
    sex: str,
    age: Optional[float] = None,
    sib_sp: Optional[int] = None,
    parch: Optional[int] = None,
    ticket: Optional[str] = None,
    fare: Optional[float] = None,
    cabin: Optional[str] = None,
    embarked: Optional[str] = None,
):

    column_dtypes = {
        "PassengerId": "int64",
        "Pclass": "int64",
        "Name": "object",
        "Sex": "object",
        "Age": "float64",
        "SibSp": "int64",
        "Parch": "int64",
        "Ticket": "object",
        "Fare": "float64",
        "Cabin": "object",
        "Embarked": "object",
    }

    object_cols = [col for col, dtype in column_dtypes.items() if dtype == "object"]
    other_cols = [col for col, dtype in column_dtypes.items() if dtype != "object"]

    input = pd.DataFrame(
        {
            "PassengerId": [1],
            "Pclass": [pclass],
            "Name": [name],
            "Sex": [sex],
            "Age": [age],
            "SibSp": [sib_sp],
            "Parch": [parch],
            "Ticket": [ticket],
            "Fare": [fare],
            "Cabin": [cabin],
            "Embarked": [embarked],
        }
    )

    input.loc[:, object_cols] = input.loc[:, object_cols].fillna("nan")
    input.loc[:, other_cols] = input.loc[:, other_cols].fillna(np.nan)

    processed_input = transformer.transform(input)
    input_proba = model.predict_proba(processed_input)

    return {
        "input_proba": (input_proba[0, 0], input_proba[0, 1])
    }
