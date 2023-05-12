from typing import Tuple, List

import numpy as np
import pandas as pd


class Preprocessor():
    """General class used for preprocessing."""

    # Mean values to fill missing data

    # Age
    age_mean: np.float64
    grouped_age_means: pd.Series
    # Fare
    fare_mean: float

    # Dummies values labels

    # Cabin numbers
    cabin_number_bins: np.ndarray
    # All dummies
    dummy_columns_values: List[str]

    def __init__(
        self,
        dummy_columns: List[str] = None,
        drop_columns: List[str] = None,
        letter_group_1: List[str] = None,
        letter_group_2: List[str] = None,
    ):

        # Ticket letter groups
        self.letter_group_1 = letter_group_1 if letter_group_1 is not None else ['1', '2', '3', 'S', 'P', 'C', 'A']
        self.letter_group_2 = letter_group_2 if letter_group_2 is not None else ['W', '4', '7', '6', 'L', '5', '8']

        self.dummy_columns = dummy_columns if dummy_columns is not None else []
        self.drop_columns = drop_columns if drop_columns is not None else []

    def process_name(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Creates two separate columns: a numeric column indicating the length of a
        passenger's Name field, and a categorical column that extracts the
        passenger's title.
        """
        df_new = df.copy()
        df_new['Name_Len'] = df_new['Name'].apply(len)
        df_new['Name_Title'] = df_new['Name'].apply(lambda x: x.split(',')[1]).apply(lambda x: x.split()[0])
        return df_new

    def _get_mean_age_if_exist(self, name_title: str, p_class: int):
        if (name_title, p_class) in self.grouped_age_means.index:
            return self.grouped_age_means[name_title, p_class]
        else:
            return self.age_mean

    def impute_age(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Imputes the null values of the Age column by filling in the mean value of
        the passenger's corresponding title and class.
        """
        df_new = df.copy()
        df_new['Age_Null_Flag'] = df_new['Age'].isnull().apply(int)
        df_new.loc[df_new['Age'].isnull(), "Age"] = df_new.loc[df_new['Age'].isnull()].apply(
            lambda x: self._get_mean_age_if_exist(x["Name_Title"], x["Pclass"]),
            axis=1
        ).copy()
        return df_new

    def size_family(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Combines the SibSp and Parch columns into a new variable that indicates
        family size, and group the family size variable into three categories.
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

    def fill_fare_na(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fills NA Fares values with fitted mean value.
        """
        df_new = df.copy()
        df_new['Fare'].fillna(self.fare_mean, inplace=True)
        return df_new

    def group_ticket(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        The Ticket column is used to create three new columns: Ticket_Letter, which
        indicates the first letter of each ticket (with the smaller-n values being
        grouped based on survival rate); Ticket_Category, which indicated the category
        of the ticket, and Ticket_Length, which indicates the length of the Ticket field.
        """
        df_new = df.copy()
        df_new['Ticket_Letter'] = df_new['Ticket'].apply(lambda x: str(x)[0])
        df_new['Ticket_Letter'] = df_new['Ticket_Letter'].apply(str)
        df_new['Ticket_Category'] = np.where(
                                    (df_new['Ticket_Letter']).isin(self.letter_group_1), df_new['Ticket_Letter'],
                                    np.where(
                                        (df_new['Ticket_Letter']).isin(self.letter_group_2), 'Low_ticket',
                                        'Other_ticket'
                                    )
                                )
        df_new['Ticket_Length'] = df_new['Ticket'].apply(len)
        return df_new

    def get_cabin_first_letter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts the first letter of the Cabin column.
        """
        df_new = df.copy()
        df_new['Cabin_Letter'] = df_new['Cabin'].apply(lambda x: str(x)[0])
        return df_new

    def get_cabin_number(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts the number of the Cabin column.
        """
        df_new = df.copy()
        df_new['Cabin_Number'] = df_new['Cabin'].apply(lambda x: str(x).split(' ')[-1][1:])
        df_new['Cabin_Number'].replace('an', np.NaN, inplace=True)
        df_new['Cabin_Number'] = df_new['Cabin_Number'].apply(
            lambda x: int(x) if not pd.isnull(x) and x != '' else np.NaN
        )
        return df_new

    def get_dummy_cabin_number(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get the category from cabin number and dummify it.
        """
        df_new = df.copy()
        dummies_cols = [f"Cabin_Number_{i}" for i in range(3)]

        df_new.loc[:, dummies_cols] = 0

        concerned_index = df_new['Cabin_Number'].dropna().index

        if df_new.loc[~df_new["Cabin_Number"].isna()].shape[0] > 0:
            categories = pd.cut(
                df_new.loc[concerned_index, 'Cabin_Number'],
                bins=self.cabin_number_bins,
                labels=False,
                include_lowest=True
            )
            df_new.loc[concerned_index, dummies_cols] = pd.get_dummies(categories, prefix="Cabin_Number")

        return df_new

    def impute_embarked(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fills the null values in the Embarked column with the most commonly
        occurring value, which is 'S'.
        """
        df_new = df.copy()
        df_new['Embarked'] = df_new['Embarked'].fillna('S')
        return df_new

    def dummy_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Converts our categorical columns into dummy variables, and then drops the
        original categorical columns. It also makes sure that each category is
        present in both the training and test datasets.
        """
        df_new = df.copy()
        df_new.loc[:, self.dummy_columns_values] = 0
        df_new.loc[:, self.dummy_columns] = df_new.loc[:, self.dummy_columns].applymap(str)

        dummies = pd.get_dummies(
            df_new[self.dummy_columns], columns=self.dummy_columns, prefix=self.dummy_columns
        )

        dummies = dummies.drop([col for col in dummies.columns if col not in self.dummy_columns_values], axis=1)

        df_new.loc[:, dummies.columns] = dummies
        return df_new

    def drop_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Drops columns in the given list.
        """
        df_new = df.copy()
        df_new = df_new.drop(self.drop_columns, axis=1)
        return df_new

    def fit_transform(self, df: pd.DataFrame):
        """
        Fits the proprocessing steps on train data and transform it.
        """
        df_new = df.copy()

        df_new = self.process_name(df=df_new)

        self.age_mean = df_new["Age"].mean()
        self.grouped_age_means = df_new.groupby(['Name_Title', 'Pclass'])['Age'].mean()
        df_new = self.impute_age(df=df_new)

        self.fare_mean = df_new['Fare'].mean()
        df_new = self.fill_fare_na(df=df_new)

        df_new = self.impute_embarked(df=df_new)
        df_new = self.size_family(df=df_new)
        df_new = self.group_ticket(df=df_new)

        df_new = self.get_cabin_number(df=df_new)
        _, self.cabin_number_bins = pd.qcut(df_new['Cabin_Number'], 3, retbins=True, labels=False)
        df_new = self.get_dummy_cabin_number(df=df_new)

        df_new = self.get_cabin_first_letter(df=df_new)
        df_new = self.get_cabin_number(df=df_new)

        self.dummy_columns_values = pd.get_dummies(
            df_new.loc[:, self.dummy_columns].applymap(str), prefix=self.dummy_columns
        ).columns

        df_new = self.dummy_cols(df=df_new)
        df_new = self.drop_cols(df=df_new)

        return df_new

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply transformations based on fitted parameters.
        """
        df_new = df.copy()

        df_new = self.process_name(df=df_new)
        df_new = self.impute_age(df=df_new)
        df_new = self.fill_fare_na(df=df_new)
        df_new = self.impute_embarked(df=df_new)
        df_new = self.size_family(df=df_new)
        df_new = self.group_ticket(df=df_new)
        df_new = self.get_cabin_number(df=df_new)
        df_new = self.get_cabin_first_letter(df=df_new)
        df_new = self.get_cabin_number(df=df_new)
        df_new = self.get_dummy_cabin_number(df=df_new)
        df_new = self.dummy_cols(df=df_new)
        df_new = self.drop_cols(df=df_new)

        return df_new


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
    preprocessor = Preprocessor(dummy_columns=dummy_columns, drop_columns=drop_columns)

    train_processed = preprocessor.fit_transform(train)
    test_processed = preprocessor.transform(test)

    return train_processed, test_processed
