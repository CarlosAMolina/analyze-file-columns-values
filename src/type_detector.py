from pandas import Series
import pandas as pd


class IntegerTypeDetector:
    def __init__(self, column: Series):
        self._column = column

    def is_column_of_this_type(self) -> bool:
        try:
            column_numeric = pd.to_numeric(self._column, errors="raise")
            if pd.api.types.is_integer_dtype(column_numeric) is True:
                return True
        except ValueError:
            return False


class DecimalTypeDetector:
    def __init__(self, column: Series):
        self._column = column

    def is_column_of_this_type(self) -> bool:
        try:
            column_numeric = pd.to_numeric(self._column, errors="raise")
            return column_numeric.dtype == "float64"
        except ValueError:
            return False


# TODO rm
def print_df(df):
    pd.set_option("display.max_columns", None)
    print(df)
