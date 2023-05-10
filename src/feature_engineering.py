from typing import Tuple, List
from abc import ABCMeta, abstractmethod

import numpy as np
import pandas as pd

from sklearn.preprocessing import KBinsDiscretizer


class Transformer(metaclass=ABCMeta):
    """Abstract class used for data preprocessing."""

    @abstractmethod
    def fit(self, X: pd.DataFrame):
        """Fits the transformation based on training data."""
        pass

    @abstractmethod
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Applies transformation after fit."""
        pass

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Fits data on X and applies the transformation."""
        self.fit(X)
        return self.transform(X)


class ProcessNameTransformer(Transformer):
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


class ImputeAgeTransformer(Transformer):
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


class SizeFamilyTransformer(Transformer):
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


class FillFareNaTransformer(Transformer):
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


class GroupTicketTransformer(Transformer):
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


class GetCabinFirstLetterTransformer(Transformer):
    """
    Extracts the first letter of the Cabin column
    """

    def fit(self, X: pd.DataFrame):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()
        X_new['Cabin_Letter'] = X_new['Cabin'].apply(lambda x: str(x)[0])
        return X_new


class GetCabinNumberTransformer(Transformer):
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


class DummyCabinNumberTransformer(Transformer):
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


class ImputeEmbarkedTransformer(Transformer):
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


class DummyColsTransformer(Transformer):
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


class DropColsTransformer(Transformer):
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


class MainTransformer(Transformer):
    """Every required transformations chained in a pipeline."""

    transformations: List[Transformer]

    def __init__(self, dummy_columns: List[str], drop_columns: List[str]):

        self.transformations = [
            ProcessNameTransformer(),
            ImputeAgeTransformer(),
            GetCabinFirstLetterTransformer(),
            ImputeEmbarkedTransformer(),
            SizeFamilyTransformer(),
            FillFareNaTransformer(),
            GroupTicketTransformer(),
            GetCabinNumberTransformer(),
            DummyCabinNumberTransformer(n_bins=3),
            DummyColsTransformer(dummy_columns=dummy_columns),
            DropColsTransformer(drop_columns=drop_columns),
        ]

    def fit(self, X: pd.DataFrame):
        X_new = X.copy()

        for transformation in self.transformations:
            X_new = transformation.fit_transform(X_new)

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X_new = X.copy()

        for transformation in self.transformations:
            X_new = transformation.transform(X_new)

        return X_new


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
    transformer = MainTransformer(dummy_columns=dummy_columns, drop_columns=drop_columns)

    transformer.fit(train)

    train_processed = transformer.transform(train)
    test_processed = transformer.transform(test)

    return train_processed, test_processed
