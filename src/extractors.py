import csv

from pandas import DataFrame as Df
import pandas as pd


def get_df_from_csv(path_name: str) -> Df:
    # Read all columns as str to not modify numeric values
    return pd.read_csv(path_name, dtype=str)


def _get_df_from_cr_csv(path_name) -> Df:
    return pd.read_csv(
        path_name,
        dtype=str,
        sep="|",
        quoting=csv.QUOTE_NONE,
        skipinitialspace=True,
        na_values=["N.A."],
    )
