import numpy as np
import pandas as pd

from src.feature_engineering import Preprocessor


def test_process_name_should_create_name_length_and_title():
    # Given
    df = pd.DataFrame({"Name": ["Braund, Mr. Owen Harris"]})
    expected_df = pd.DataFrame(
        {
            "Name": ["Braund, Mr. Owen Harris"],
            "Name_Len": [23],
            "Name_Title": ["Mr."],
        }
    )
    preprocessor = Preprocessor()

    # When
    result_df = preprocessor.process_name(df)

    # Then
    pd.testing.assert_frame_equal(expected_df, result_df)


def test_impute_age_should_fill_missing_ages_with_learned_means():
    # Given
    df = pd.DataFrame(
        {
            "Age": [22.0, np.nan, np.nan],
            "Name_Title": ["Mr.", "Mr.", "Mrs."],
            "Pclass": [3, 3, 1],
        }
    )
    preprocessor = Preprocessor()
    # Paramètres normalement appris par fit_transform sur le jeu d'entraînement.
    preprocessor.grouped_age_means = pd.Series({("Mr.", 3): 30.0})
    preprocessor.age_mean = 25.0

    # When
    result_df = preprocessor.impute_age(df)

    # Then
    assert result_df["Age"].tolist() == [22.0, 30.0, 25.0]
    assert result_df["Age_Null_Flag"].tolist() == [0, 1, 1]
