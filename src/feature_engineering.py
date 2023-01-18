from typing import Tuple

import numpy as np
import pandas as pd


def process_name(train: pd.DataFrame, test: pd.DataFrame):
    """
    Creates two separate columns: a numeric column indicating the length of a
    passenger's Name field, and a categorical column that extracts the
    passenger's title.

    Args:
        train: The train set
        test: The test set

    """
    for df in [train, test]:
        df['Name_Len'] = df['Name'].apply(lambda x: len(x))
        df['Name_Title'] = df['Name'].apply(lambda x: x.split(',')[1]).apply(lambda x: x.split()[0])


def impute_age(train: pd.DataFrame, test: pd.DataFrame):
    """
    Imputes the null values of the Age column by filling in the mean value of
    the passenger's corresponding title and class.

    Args:
        train: The train set
        test: The test set

    """
    for df in [train, test]:
        df['Age_Null_Flag'] = df['Age'].apply(lambda x: 1 if pd.isnull(x) else 0)
        data = train.groupby(['Name_Title', 'Pclass'])['Age']
        df['Age'] = data.transform(lambda x: x.fillna(x.mean()))


def size_family(train: pd.DataFrame, test: pd.DataFrame):
    """
    Combines the SibSp and Parch columns into a new variable that indicates
    family size, and group the family size variable into three categories.

    Args:
        train: The train set
        test: The test set

    """
    for df in [train, test]:
        df['Family_Size'] = np.where((df['SibSp'] + df['Parch']) == 0, 'Solo',
                                     np.where((df['SibSp'] + df['Parch']) <= 3, 'Nuclear', 'Big'))


def group_ticket(train: pd.DataFrame, test: pd.DataFrame):
    """
    The Ticket column is used to create three new columns: Ticket_Letter, which
    indicates the first letter of each ticket (with the smaller-n values being
    grouped based on survival rate); Ticket_Category, which indicated the category
    of the ticket, and Ticket_Length, which indicates the length of the Ticket field.

    Args:
        train: The train set
        test: The test set

    """
    letter_group_1 = ['1', '2', '3', 'S', 'P', 'C', 'A']
    letter_group_2 = ['W', '4', '7', '6', 'L', '5', '8']
    for df in [train, test]:
        df['Ticket_Letter'] = df['Ticket'].apply(lambda x: str(x)[0])
        df['Ticket_Letter'] = df['Ticket_Letter'].apply(lambda x: str(x))
        df['Ticket_Category'] = np.where((df['Ticket_Letter']).isin(letter_group_1), df['Ticket_Letter'],
                                         np.where((df['Ticket_Letter']).isin(letter_group_2),
                                                  'Low_ticket', 'Other_ticket'))
        df['Ticket_Length'] = df['Ticket'].apply(lambda x: len(x))


def get_cabin_first_letter(train: pd.DataFrame, test: pd.DataFrame):
    """
    Extracts the first letter of the Cabin column

    Args:
        train: The train set
        test: The test set

    """
    for df in [train, test]:
        df['Cabin_Letter'] = df['Cabin'].apply(lambda x: str(x)[0])


def dummy_cabin_number(train: pd.DataFrame, test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extracts the number of the Cabin column, get the category and dummify it

    Args:
        train: The train set
        test: The test set

    Returns:
        new_train
        new_test

    """
    for df in [train, test]:
        df['Cabin_Number'] = df['Cabin'].apply(lambda x: str(x).split(' ')[-1][1:])
        df['Cabin_Number'].replace('an', np.NaN, inplace=True)
        df['Cabin_Number'] = df['Cabin_Number'].apply(lambda x: int(x) if not pd.isnull(x) and x != '' else np.NaN)
        df['Cabin_Number_Category'] = pd.qcut(train['Cabin_Number'], 3)
    train_dummy = pd.concat((train, pd.get_dummies(train['Cabin_Number_Category'], prefix='Cabin_Number')), axis=1)
    test_dummy = pd.concat((test, pd.get_dummies(test['Cabin_Number_Category'], prefix='Cabin_Number')), axis=1)

    return train_dummy, test_dummy


def impute_embarked(train: pd.DataFrame, test: pd.DataFrame):
    """
    Fills the null values in the Embarked column with the most commonly
    occuring value, which is 'S.'

    Args:
        train: The train set
        test: The test set

    """
    for df in [train, test]:
        df['Embarked'] = df['Embarked'].fillna('S')


def dummies(train: pd.DataFrame, test: pd.DataFrame, dummy_columns: list):
    """
    Converts our categorical columns into dummy variables, and then drops the
    original categorical columns. It also makes sure that each category is
    present in both the training and test datasets.

    Args:
        train: The train set
        test: The test set
        dummy_columns: The columns to be dummified. If None is passed,
            default values are applied.

    Returns:
        new_train
        new_test

    """
    for column in dummy_columns:
        train[column] = train[column].apply(lambda x: str(x))
        test[column] = test[column].apply(lambda x: str(x))

        good_cols = [column + '_' + i for i in train[column].unique() if i in test[column].unique()]
        train = pd.concat((train, pd.get_dummies(train[column], prefix=column)[good_cols]), axis=1)
        test = pd.concat((test, pd.get_dummies(test[column], prefix=column)[good_cols]), axis=1)
    return train, test


def drop(train: pd.DataFrame, test: pd.DataFrame, drop_columns: list):
    """
    Drops columns in the given list

    Args:
        train: The train set
        test: The test set
        drop_columns: The columns to be dropped. If None is passed,
            default values are applied.

    """
    for df in [train, test]:
        df.drop(drop_columns, inplace=True, axis=1)


def process_data(train: pd.DataFrame, test: pd.DataFrame, dummy_columns: list, drop_columns: list) -> Tuple[
    pd.DataFrame, pd.DataFrame]:
    """
    Apply all neccessary transformations to clean train and test data

    Args:
        train: The train set
        test: The test set
        drop_columns: The columns to be dropped. If None is passed,
            default values are applied.
        dummy_columns: The columns to be dummified. If None is passed,
            default values are applied.

    Returns:
        new_train
        new_test

    """
    train_cp = train.copy()
    test_cp = test.copy()
    process_name(train_cp, test_cp)
    impute_age(train_cp, test_cp)
    get_cabin_first_letter(train_cp, test_cp)
    impute_embarked(train_cp, test_cp)
    size_family(train_cp, test_cp)
    test_cp['Fare'].fillna(train['Fare'].mean(), inplace=True)
    group_ticket(train_cp, test_cp)
    train_dummy_cabin, test_dummy_cabin = dummy_cabin_number(train_cp, test_cp)
    train_processed, test_processed = dummies(train_dummy_cabin, test_dummy_cabin, dummy_columns)
    drop(train_processed, test_processed, drop_columns)

    return train_processed, test_processed
