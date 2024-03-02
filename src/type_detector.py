import typing as tp

from pandas import Series
import pandas as pd


class IntegerTypeDetector:
    def __init__(self, column_strings: Series):
        self._column_strings = column_strings

    def is_column_of_this_type(self) -> bool:
        column_numeric = _get_column_as_numeric(self._column_strings)
        if column_numeric is None:
            return False
        else:
            return pd.api.types.is_integer_dtype(column_numeric)


class DecimalTypeDetector:
    def __init__(self, column_strings: Series):
        self._column_strings = column_strings

    def is_column_of_this_type(self) -> bool:
        column_numeric = _get_column_as_numeric(self._column_strings)
        if column_numeric is None:
            return False
        else:
            return column_numeric.dtype == "float64"


def _get_column_as_numeric(column: Series) -> tp.Optional[Series]:
    try:
        return pd.to_numeric(column, errors="raise")
    except ValueError:
        return None


# TODO rm
def print_df(df):
    pd.set_option("display.max_columns", None)
    print(df)
