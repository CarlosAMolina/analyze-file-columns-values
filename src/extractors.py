import csv

from pandas import DataFrame as Df
import pandas as pd


def get_df_from_csv(path_name: str) -> Df:
    # Read all columns as str to not modify numeric values
    return pd.read_csv(path_name, dtype=str)
    # return _get_df_from_cr_csv(path_name)


def _get_df_from_cr_csv(path_name) -> Df:
    from src import constants

    return pd.read_csv(
        path_name,
        dtype=str,
        sep="|",
        names=constants.COLUMN_NAMES,
        quoting=csv.QUOTE_NONE,
        skipinitialspace=True,
        na_values=["N.A."],
        usecols=constants.COLUMN_NAMES_TO_USE,
    )
