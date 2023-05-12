import numpy as np
import pandas as pd

from src.feature_engineering import Preprocessor


def test_process_name_should_create_column_name_lenght():
    # Given
    test = pd.DataFrame(
        {
            "Name":
                ['Kelly, Mr. James',
                 'Wilkes, Mrs. James (Ellen Needs)',
                 'Myles, Mr. Thomas Francis',
                 'Wirz, Mr. Albert',
                 'Hirvonen, Mrs. Alexander (Helga E Lindqvist)']
        })
    expected_test_lenght = [16, 32, 25, 16, 44]

    # When
    preprocessor = Preprocessor()
    test = preprocessor.process_name(test)

    # Then
    assert "Name_Len" in test.columns
    assert test["Name_Len"].tolist() == expected_test_lenght


def test_process_name_should_create_column_name_title():
    # Given
    test = pd.DataFrame(
        {
            "Name":
                ['Kelly, Mr. James',
                 'Wilkes, Mrs. James (Ellen Needs)',
                 'Myles, Mr. Thomas Francis',
                 'Wirz, Mr. Albert',
                 'Hirvonen, Mrs. Alexander (Helga E Lindqvist)']
        })
    expected_test_titles = ["Mr.", "Mrs.", "Mr.", "Mr.", "Mrs."]

    # When
    preprocessor = Preprocessor()
    test = preprocessor.process_name(test)

    # Then
    assert "Name_Title" in test.columns
    assert test["Name_Title"].tolist() == expected_test_titles


def test_impute_age_should_create_2_columns_age_and_age_null_flag():
    # Given
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    preprocessor = Preprocessor()

    # impute age reffers to fitted parameters.
    preprocessor.grouped_age_means = pd.Series(dtype='object')
    preprocessor.age_mean = 0

    # When
    test = preprocessor.impute_age(test)

    # Then
    assert "Age" in test.columns
    assert "Age_Null_Flag" in test.columns


def test_impute_age_should_set_age_column_without_missing_value():
    # Given
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    preprocessor = Preprocessor()

    # impute age reffers to fitted parameters.
    preprocessor.grouped_age_means = pd.Series(dtype='object')
    preprocessor.age_mean = 0

    # When
    test = preprocessor.impute_age(test)

    # Then
    assert test["Age"].notnull().all()


def test_age_impute_should_return_dataframe_binary_age_null_flag():
    # Given
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    preprocessor = Preprocessor()

    # impute age reffers to fitted parameters.
    preprocessor.grouped_age_means = pd.Series(dtype='object')
    preprocessor.age_mean = 0

    # When
    test = preprocessor.impute_age(test)

    # Then
    assert set(test["Age_Null_Flag"].unique()) == {0, 1}


def test_impute_age_should_flag_null_values_in_age_column():
    # Given
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    preprocessor = Preprocessor()

    # impute age reffers to fitted parameters.
    preprocessor.grouped_age_means = pd.Series(dtype='object')
    preprocessor.age_mean = 0

    # When
    test = preprocessor.impute_age(test)

    # Then
    assert test["Age_Null_Flag"].tolist() == [0, 0, 0, 0, 1]
