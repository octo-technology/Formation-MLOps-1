import numpy as np
import pandas as pd

from src.feature_engineering import process_name, impute_age


def test_process_name_should_create_column_name_length():
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
    expected_test_length = [16, 32, 25, 16, 44]

    # When
    test = process_name(test)

    # Then
    assert "Name_Len" in test.columns
    assert test["Name_Len"].tolist() == expected_test_length


def test_names_should_create_column_name_title():
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
    test = process_name(test)

    # Then
    assert "Name_Title" in test.columns
    assert test["Name_Title"].tolist() == expected_test_titles


def test_age_impute_should_create_2_columns_age_and_age_null_flag():
    # Given
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    # impute age reffers to fitted parameters.
    grouped_age_means = pd.Series(dtype='object')
    age_mean = 0

    # When
    test = impute_age(test, age_mean=age_mean, grouped_age_means=grouped_age_means)

    # Then
    assert "Age" in test.columns
    assert "Age_Null_Flag" in test.columns


def test_age_impute_should_set_age_column_without_missing_value():
    # Given
    # note : at least one pair Title-Pclass covering the null case should exist
    # in the train set
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    # impute age reffers to fitted parameters.
    grouped_age_means = pd.Series(dtype='object')
    age_mean = 0

    # When
    test = impute_age(test, age_mean=age_mean, grouped_age_means=grouped_age_means)

    # Then
    assert test["Age"].notnull().all()


def test_age_impute_should_set_age_null_flag_column_with_binary_value():
    # Given
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    # impute age reffers to fitted parameters.
    grouped_age_means = pd.Series(dtype='object')
    age_mean = 0

    # When
    test = impute_age(test, age_mean=age_mean, grouped_age_means=grouped_age_means)

    # Then
    assert set(test["Age_Null_Flag"].unique()) == {0, 1}


def test_age_impute_should_flag_null_values_in_age_column():
    # Given
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    # impute age reffers to fitted parameters.
    grouped_age_means = pd.Series(dtype='object')
    age_mean = 0

    # When
    test = impute_age(test, age_mean=age_mean, grouped_age_means=grouped_age_means)

    # Then
    assert test["Age_Null_Flag"].tolist() == [0, 0, 0, 0, 1]
