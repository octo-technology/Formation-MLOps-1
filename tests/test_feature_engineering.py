import numpy as np
import pandas as pd

from src.feature_engineering import process_name, impute_age


def test_process_name_should_create_column_name_lenght():
    # Given
    train = pd.DataFrame(
        {
            "Name":
                ['Braund, Mr. Owen Harris',
                 'Cumings, Mrs. John Bradley '
                 '(Florence Briggs Thayer)',
                 'Heikkinen, Miss. Laina',
                 'Futrelle, Mrs. Jacques Heath (Lily May Peel)',
                 'Allen, Mr. William Henry']
        })
    expected_train_length = [23, 51, 22, 44, 24]
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
    process_name(train, test)

    # Then
    assert "Name_Len" in train.columns
    assert "Name_Len" in test.columns
    assert train["Name_Len"].tolist() == expected_train_length
    assert test["Name_Len"].tolist() == expected_test_lenght



def test_process_name_should_create_column_name_title():
    # Given
    train = pd.DataFrame(
        {
            "Name":
                ['Braund, Mr. Owen Harris',
                 'Cumings, Mrs. John Bradley '
                 '(Florence Briggs Thayer)',
                 'Heikkinen, Miss. Laina',
                 'Futrelle, Mrs. Jacques Heath (Lily May Peel)',
                 'Allen, Mr. William Henry']
        })
    expected_train_titles = ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."]
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
    process_name(train, test)

    # Then
    assert "Name_Title" in train.columns
    assert "Name_Title" in test.columns
    assert train["Name_Title"].tolist() == expected_train_titles
    assert test["Name_Title"].tolist() == expected_test_titles


def test_impute_age_should_create_2_columns_age_and_age_null_flag():
    # Given
    train = pd.DataFrame(
        {
            "Age": [12, 52, 23, np.nan, 42],
            "Name_Title": ["Mr.", "Mrs.", "Mr.", "Mr.", "Mrs."],
            "Pclass": [0, 1, 2, 1, 0]
        })
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    # When
    impute_age(train, test)

    # Then
    assert "Age" in train.columns
    assert "Age" in test.columns
    assert "Age_Null_Flag" in train.columns
    assert "Age_Null_Flag" in test.columns



def test_impute_age_should_set_age_column_without_missing_value():
    # Given
    # note : at least one pair Title-Pclass covering the null case should exist
    # in the train set
    train = pd.DataFrame(
        {
            "Age": [12, 52, 23, np.nan, 42],
            "Name_Title": ["Mr.", "Mrs.", "Mr.", "Mr.", "Mrs."],
            "Pclass": [0, 1, 2, 2, 0]
        })
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    # When
    impute_age(train, test)

    # Then
    assert train["Age"].notnull().all()
    assert test["Age"].notnull().all()



def test_age_impute_should_return_dataframe_binary_age_null_flag():
    # Given
    train = pd.DataFrame(
        {
            "Age": [12, 52, 23, np.nan, 42],
            "Name_Title": ["Mr.", "Mrs.", "Mr.", "Mr.", "Mrs."],
            "Pclass": [0, 1, 2, 1, 0]
        })
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    # When
    impute_age(train, test)

    # Then
    for output in (train, test):
        assert set(output["Age_Null_Flag"].unique()) == {0, 1}


def test_impute_age_should_flag_null_values_in_age_column():
    # Given
    train = pd.DataFrame(
        {
            "Age": [12, 52, 23, np.nan, 42],
            "Name_Title": ["Mr.", "Mrs.", "Mr.", "Mr.", "Mrs."],
            "Pclass": [0, 1, 2, 1, 0]
        })
    test = pd.DataFrame(
        {
            "Age": [7, 14, 120, 31, np.nan],
            "Name_Title": ["Mr.", "Mrs.", "Miss.", "Mrs.", "Mr."],
            "Pclass": [2, 0, 2, 1, 0]
        })

    # When
    impute_age(train, test)

    # Then
    assert train["Age_Null_Flag"].tolist() == [0, 0, 0, 1, 0]
    assert test["Age_Null_Flag"].tolist() == [0, 0, 0, 0, 1]

