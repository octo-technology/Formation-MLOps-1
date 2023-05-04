from typing import Tuple, List

import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import KBinsDiscretizer


class ProcessNameTransformer(BaseEstimator, TransformerMixin):
    """
    Creates two separate columns: a numeric column indicating the length of a
    passenger's Name field, and a categorical column that extracts the
    passenger's title.
    """

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new['Name_Len'] = X_new['Name'].apply(len)
        X_new['Name_Title'] = X_new['Name'].apply(lambda x: x.split(',')[1]).apply(lambda x: x.split()[0])
        return X_new


class ImputeAgeTransformer(BaseEstimator, TransformerMixin):
    """
    Imputes the null values of the Age column by filling in the mean value of
    the passenger's corresponding title and class.
    """

    age_mean: np.float64
    grouped_age_means: pd.Series

    def _get_mean_age_if_exist(self, name_title: str, p_class: int):
        if (name_title, p_class) in self.grouped_age_means.index:
            return self.grouped_age_means[name_title, p_class]
        else:
            return self.age_mean

    def fit(self, X: pd.DataFrame):
        self.age_mean = X["Age"].mean()
        self.grouped_age_means = X.groupby(['Name_Title', 'Pclass'])['Age'].mean().copy()

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new['Age_Null_Flag'] = X_new['Age'].isnull().apply(int)
        X_new.loc[X_new['Age'].isnull(), "Age"] = X_new.loc[X_new['Age'].isnull()].apply(
            lambda x: self._get_mean_age_if_exist(x["Name_Title"], x["Pclass"]),
            axis=1
        ).copy()

        return X_new


class SizeFamilyTransformer(BaseEstimator, TransformerMixin):
    """
    Combines the SibSp and Parch columns into a new variable that indicates
    family size, and group the family size variable into three categories.
    """

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new['Family_Size'] = np.where(
            (X_new['SibSp'] + X_new['Parch']) == 0, 'Solo',
            np.where(
                (X_new['SibSp'] + X_new['Parch']) <= 3, 'Nuclear',
                'Big'
            )
        )
        return X_new


class FillFareNaTransformer(BaseEstimator, TransformerMixin):
    """
    Fills NA Fares values with fitted mean value.
    """

    mean_fare: float

    def fit(self, X: pd.DataFrame):
        self.mean_fare = X['Fare'].mean()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new['Fare'].fillna(self.mean_fare, inplace=True)
        return X_new


class GroupTicketTransformer(BaseEstimator, TransformerMixin):
    """
    The Ticket column is used to create three new columns: Ticket_Letter, which
    indicates the first letter of each ticket (with the smaller-n values being
    grouped based on survival rate); Ticket_Category, which indicated the category
    of the ticket, and Ticket_Length, which indicates the length of the Ticket field.
    """

    def __init__(self, letter_group_1: List[str] = None, letter_group_2: List[str] = None):
        self.letter_group_1 = letter_group_1 if letter_group_1 is not None else ['1', '2', '3', 'S', 'P', 'C', 'A']
        self.letter_group_2 = letter_group_2 if letter_group_2 is not None else ['W', '4', '7', '6', 'L', '5', '8']

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new['Ticket_Letter'] = X_new['Ticket'].apply(lambda x: str(x)[0])
        X_new['Ticket_Letter'] = X_new['Ticket_Letter'].apply(str)
        X_new['Ticket_Category'] = np.where(
                                    (X_new['Ticket_Letter']).isin(self.letter_group_1), X_new['Ticket_Letter'],
                                    np.where(
                                        (X_new['Ticket_Letter']).isin(self.letter_group_2), 'Low_ticket',
                                        'Other_ticket'
                                    )
                                )
        X_new['Ticket_Length'] = X_new['Ticket'].apply(len)
        return X_new


class GetCabinFirstLetterTransformer(BaseEstimator, TransformerMixin):
    """
    Extracts the first letter of the Cabin column
    """

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new['Cabin_Letter'] = X_new['Cabin'].apply(lambda x: str(x)[0])
        return X_new


class GetCabinNumberTransformer(BaseEstimator, TransformerMixin):
    """
    Extracts the number of the Cabin column
    """

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new['Cabin_Number'] = X_new['Cabin'].apply(lambda x: str(x).split(' ')[-1][1:])
        X_new['Cabin_Number'].replace('an', np.NaN, inplace=True)
        X_new['Cabin_Number'] = X_new['Cabin_Number'].apply(
            lambda x: int(x) if not pd.isnull(x) and x != '' else np.NaN
        )
        return X_new


class DummyCabinNumberTransformer(BaseEstimator, TransformerMixin):
    """
    Get the category from cabin number and dummify it
    """
    def __init__(self, n_bins=3):
        self.n_bins = n_bins
        self.kbins_discretizer = KBinsDiscretizer(n_bins=n_bins, encode="onehot-dense", strategy="quantile")

    def fit(self, X: pd.DataFrame):
        self.kbins_discretizer = self.kbins_discretizer.fit(X['Cabin_Number'].dropna().values.reshape(-1, 1))
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        dummies_cols = [f"Cabin_Number_{i}" for i in range(self.n_bins)]

        X_new.loc[:, dummies_cols] = 0

        if X_new.loc[~X["Cabin_Number"].isna()].shape[0] > 0:
            one_hot = self.kbins_discretizer.transform(X_new['Cabin_Number'].dropna().values.reshape(-1, 1))
            X_new.loc[~X["Cabin_Number"].isna(), dummies_cols] = one_hot

        return X_new


class ImputeEmbarkedTransformer(BaseEstimator, TransformerMixin):
    """
    Fills the null values in the Embarked column with the most commonly
    occurring value, which is 'S.'
    """

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new['Embarked'] = X_new['Embarked'].fillna('S')
        return X_new


class DummyColsTransformer(BaseEstimator, TransformerMixin):
    """
    Converts our categorical columns into dummy variables, and then drops the
    original categorical columns. It also makes sure that each category is
    present in both the training and test datasets.
    """
    def __init__(self, dummy_columns):
        self.columns = None
        self.dummy_columns = dummy_columns

    def fit(self, X: pd.DataFrame):
        self.columns = pd.get_dummies(X.loc[:, self.dummy_columns].applymap(str), prefix=self.dummy_columns).columns
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new.loc[:, self.columns] = 0
        X_new.loc[:, self.dummy_columns] = X_new.loc[:, self.dummy_columns].applymap(str)

        dummies = pd.get_dummies(
            X_new[self.dummy_columns], columns=self.dummy_columns, prefix=self.dummy_columns
        )

        dummies = dummies.drop([col for col in dummies.columns if col not in self.columns], axis=1)

        X_new.loc[:, dummies.columns] = dummies
        return X_new


class DropColsTransformer(BaseEstimator, TransformerMixin):
    """
    Drops columns in the given list
    """
    def __init__(self, drop_columns: List[str]):
        """
        Args:
            drop_columns: The columns to be dropped. If None is passed,
                default values are applied.
        """
        self.drop_columns = drop_columns

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new.drop(self.drop_columns, inplace=True, axis=1)
        return X_new


def get_preprocessing_pipeline(dummy_columns: List[str], drop_columns: List[str]) -> Pipeline:
    """
    Returns a sklearn transformation pipeline to perform proprocessing of train and test datasets

    Args:
        dummy_columns: The columns to be dummified.
        drop_columns: The columns to be dropped.

    Returns:
        pipe: A pipeline instance of type sklearn.pipeline.Pipeline.
    """

    pipe = Pipeline(
        [
            ("process_name_transformer", ProcessNameTransformer()),
            ("impute_age_transformer", ImputeAgeTransformer()),
            ("get_cabin_first_letter_transformer", GetCabinFirstLetterTransformer()),
            ("impute_embarked_transformer", ImputeEmbarkedTransformer()),
            ("size_family_transformer", SizeFamilyTransformer()),
            ("fill_fare_na_transformer", FillFareNaTransformer()),
            ("group_ticket_transformer", GroupTicketTransformer()),
            ("get_cabin_number_transformer", GetCabinNumberTransformer()),
            ("dummy_cabin_number_transformer", DummyCabinNumberTransformer(n_bins=3)),
            ("dummy_cols_transformer", DummyColsTransformer(dummy_columns=dummy_columns)),
            ("drop_cols_transformer", DropColsTransformer(drop_columns=drop_columns)),
        ]
    )

    return pipe


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
    pipe = get_preprocessing_pipeline(dummy_columns=dummy_columns, drop_columns=drop_columns)

    pipe.fit(train)

    train_processed = pipe.transform(train)
    test_processed = pipe.transform(test)

    return train_processed, test_processed
