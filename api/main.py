import os
import pickle
from typing import Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI
from sklearn.ensemble._forest import RandomForestClassifier

from models import MODELS_PATH
from src.feature_engineering import Preprocessor

app = FastAPI()

with open(os.path.join(MODELS_PATH, "model_rf.pkl"), "rb") as file_in:
    model: RandomForestClassifier = pickle.load(file_in)

with open(os.path.join(MODELS_PATH, "preprocessor.pkl"), "rb") as file_in:
    preprocessor: Preprocessor = pickle.load(file_in)

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


def fillna(df: pd.DataFrame) -> pd.DataFrame:
    """Replace missing values by the correct value."""

    df.loc[:, object_cols] = df.loc[:, object_cols].fillna("nan")
    df.loc[:, other_cols] = df.loc[:, other_cols].fillna(np.nan)

    return df


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

    input = fillna(df=input)

    processed_input: pd.DataFrame = preprocessor.transform(input)
    input_proba: np.ndarray = model.predict_proba(processed_input)

    return {
        "input_proba": (round(input_proba[0, 0], 10), round(input_proba[0, 1], 10))
    }
