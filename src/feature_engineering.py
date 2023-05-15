from typing import Tuple, List

import numpy as np
import pandas as pd


def process_name(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates two separate columns: a numeric column indicating the length of a
    passenger's Name field, and a categorical column that extracts the
    passenger's title.

    Args:
        df: The train or test set

    """
    df_new = df.copy()
    df_new['Name_Len'] = df_new['Name'].apply(len)
    df_new['Name_Title'] = df_new['Name'].apply(lambda x: x.split(',')[1]).apply(lambda x: x.split()[0])
    return df_new


def _get_mean_age_if_exist(name_title: str, p_class: int, age_mean: np.float64, grouped_age_means: pd.Series):
    """
    Given a title and class returns train set mean age if known, else global train set mean age.

    Args:
        name_title: Passenger title
        p_class: Passenger class
        age_mean: Global train set mean age
        grouped_age_means: Train set mean age given a name title and p class

    """
    if (name_title, p_class) in grouped_age_means.index:
        return grouped_age_means[name_title, p_class]
    else:
        return age_mean


def impute_age(df: pd.DataFrame, age_mean: np.float64, grouped_age_means: pd.Series) -> pd.DataFrame:
    """
    Imputes the null values of the Age column by filling in the mean value of
    the passenger's corresponding title and class.

    Args:
        df: The train or test set
        age_mean: Global train set mean age
        grouped_age_means: Train set mean age given a name title and p class

    """
    df_new = df.copy()
    df_new['Age_Null_Flag'] = df_new['Age'].isnull().apply(int)
    df_new.loc[df_new['Age'].isnull(), "Age"] = df_new.loc[df_new['Age'].isnull()].apply(
        lambda x: _get_mean_age_if_exist(x["Name_Title"], x["Pclass"], age_mean, grouped_age_means),
        axis=1
    ).copy()
    return df_new


def size_family(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combines the SibSp and Parch columns into a new variable that indicates
    family size, and group the family size variable into three categories.

    Args:
        df: The train or test set

    """
    df_new = df.copy()
    df_new['Family_Size'] = np.where(
        (df_new['SibSp'] + df_new['Parch']) == 0, 'Solo',
        np.where(
            (df_new['SibSp'] + df_new['Parch']) <= 3, 'Nuclear',
            'Big'
        )
    )
    return df_new


def fill_fare_na(df: pd.DataFrame, fare_mean: float) -> pd.DataFrame:
    """
    Fills NA Fares values with fitted mean value.

    Args:
        df: The train or test set
        fare_mean: Train set mean fare

    """
    df_new = df.copy()
    df_new['Fare'].fillna(fare_mean, inplace=True)
    return df_new


def group_ticket(df: pd.DataFrame) -> pd.DataFrame:
    """
    The Ticket column is used to create three new columns: Ticket_Letter, which
    indicates the first letter of each ticket (with the smaller-n values being
    grouped based on survival rate); Ticket_Category, which indicated the category
    of the ticket, and Ticket_Length, which indicates the length of the Ticket field.

    Args:
        df: The train or test set

    """
    letter_group_1 = ['1', '2', '3', 'S', 'P', 'C', 'A']
    letter_group_2 = ['W', '4', '7', '6', 'L', '5', '8']

    df_new = df.copy()
    df_new['Ticket_Letter'] = df_new['Ticket'].apply(lambda x: str(x)[0])
    df_new['Ticket_Letter'] = df_new['Ticket_Letter'].apply(str)
    df_new['Ticket_Category'] = np.where(
                                (df_new['Ticket_Letter']).isin(letter_group_1), df_new['Ticket_Letter'],
                                np.where(
                                    (df_new['Ticket_Letter']).isin(letter_group_2), 'Low_ticket',
                                    'Other_ticket'
                                )
                            )
    df_new['Ticket_Length'] = df_new['Ticket'].apply(len)
    return df_new


def get_cabin_first_letter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts the first letter of the Cabin column.

    Args:
        df: The train or test set

    """
    df_new = df.copy()
    df_new['Cabin_Letter'] = df_new['Cabin'].apply(lambda x: str(x)[0])
    return df_new


def get_cabin_number(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts the number of the Cabin column.

    Args:
        df: The train or test set

    """
    df_new = df.copy()
    df_new['Cabin_Number'] = df_new['Cabin'].apply(lambda x: str(x).split(' ')[-1][1:])
    df_new['Cabin_Number'].replace('an', np.NaN, inplace=True)
    df_new['Cabin_Number'] = df_new['Cabin_Number'].apply(
        lambda x: int(x) if not pd.isnull(x) and x != '' else np.NaN
    )
    return df_new


def get_dummy_cabin_number(df: pd.DataFrame, cabin_number_bins: np.ndarray) -> pd.DataFrame:
    """
    Get the category from cabin number and dummify it.

    Args:
        df: The train or test set
        cabin_number_bins: Cabin nubers categories

    """
    df_new = df.copy()
    dummies_cols = [f"Cabin_Number_{i}" for i in range(3)]

    df_new.loc[:, dummies_cols] = 0

    concerned_index = df_new['Cabin_Number'].dropna().index

    if df_new.loc[~df_new["Cabin_Number"].isna()].shape[0] > 0:
        categories = pd.cut(
            df_new.loc[concerned_index, 'Cabin_Number'],
            bins=cabin_number_bins,
            labels=False,
            include_lowest=True
        )
        df_new.loc[concerned_index, dummies_cols] = pd.get_dummies(categories, prefix="Cabin_Number")

    return df_new


def impute_embarked(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills the null values in the Embarked column with the most commonly
    occurring value, which is 'S'.

    Args:
        df: The train or test set

    """
    df_new = df.copy()
    df_new['Embarked'] = df_new['Embarked'].fillna('S')
    return df_new


def dummy_cols(df: pd.DataFrame, dummy_columns: List[str], dummy_columns_values: List[str]) -> pd.DataFrame:
    """
    Converts our categorical columns into dummy variables, and then drops the
    original categorical columns. It also makes sure that each category is
    present in both the training and test datasets.

    Args:
        df: The train or test set
        dummy_columns: The columns to be dummified.
        dummy_columns_values: The dummified columns values
            Each different value from the train set dummy columns correspond to one feature.

    """
    df_new = df.copy()
    df_new.loc[:, dummy_columns_values] = 0
    df_new.loc[:, dummy_columns] = df_new.loc[:, dummy_columns].applymap(str)

    dummies = pd.get_dummies(
        df_new[dummy_columns], columns=dummy_columns, prefix=dummy_columns
    )

    dummies = dummies.drop([col for col in dummies.columns if col not in dummy_columns_values], axis=1)

    df_new.loc[:, dummies.columns] = dummies
    return df_new


def drop_cols(df: pd.DataFrame, drop_columns: List[str]) -> pd.DataFrame:
    """
    Drops columns in the given list.

    Args:
        df: The train or test set
        drop_columns: The columns to be dropped.

    """
    df_new = df.copy()
    df_new = df_new.drop(drop_columns, axis=1)
    return df_new


def process_data(train: pd.DataFrame, test: pd.DataFrame, dummy_columns: list, drop_columns: list) -> Tuple[
        pd.DataFrame, pd.DataFrame]:
    """
    Apply all neccessary transformations to clean train and test data

    Args:
        train: The train set
        test: The test set
        drop_columns: The columns to be dropped.
        dummy_columns: The columns to be dummified.

    Returns:
        new_train
        new_test

    """
    train_processed = train.copy()
    test_processed = test.copy()

    train_processed = process_name(train_processed)
    test_processed = process_name(test_processed)

    # Compute mean values from train
    age_mean = train_processed["Age"].mean()
    grouped_age_means = train_processed.groupby(['Name_Title', 'Pclass'])['Age'].mean()

    fare_mean = train_processed['Fare'].mean()

    train_processed = impute_age(train_processed, age_mean, grouped_age_means)
    test_processed = impute_age(test_processed, age_mean, grouped_age_means)

    train_processed = fill_fare_na(train_processed, fare_mean)
    test_processed = fill_fare_na(test_processed, fare_mean)

    train_processed = impute_embarked(train_processed)
    test_processed = impute_embarked(test_processed)

    train_processed = size_family(train_processed)
    test_processed = size_family(test_processed)

    train_processed = group_ticket(train_processed)
    test_processed = group_ticket(test_processed)

    train_processed = get_cabin_number(train_processed)
    test_processed = get_cabin_number(test_processed)

    # Compute cabin number bins from train
    _, cabin_number_bins = pd.qcut(train_processed['Cabin_Number'], 3, retbins=True, labels=False)

    train_processed = get_dummy_cabin_number(train_processed, cabin_number_bins)
    test_processed = get_dummy_cabin_number(test_processed, cabin_number_bins)

    train_processed = get_cabin_first_letter(train_processed)
    test_processed = get_cabin_first_letter(test_processed)

    train_processed = get_cabin_number(train_processed)
    test_processed = get_cabin_number(test_processed)

    # Compute dummy column values from train
    dummy_columns_values = pd.get_dummies(
        train_processed.loc[:, dummy_columns].applymap(str), prefix=dummy_columns
    ).columns

    train_processed = dummy_cols(train_processed, dummy_columns, dummy_columns_values)
    test_processed = dummy_cols(test_processed, dummy_columns, dummy_columns_values)

    train_processed = drop_cols(train_processed, drop_columns)
    test_processed = drop_cols(test_processed, drop_columns)

    return train_processed, test_processed
