import re
import typing as tp

from pandas import Series
import pandas as pd


def is_integer(column_strings: Series):
    return _IntegerTypeDetector(column_strings).is_column_of_this_type()


def is_decimal(column_strings: Series):
    return _DecimalTypeDetector(column_strings).is_column_of_this_type()


REGEX_DECIMAL_SEPARATOR = r"\."


class _IntegerTypeDetector:
    def __init__(self, column_strings: Series):
        self._column_strings = column_strings

    def is_column_of_this_type(self) -> bool:
        if _is_numeric_column(self._column_strings) is False:
            return False
        elif self._has_any_character():
            return False
        elif self._has_any_decimal_separator():
            return False
        return True

    def _has_any_character(self) -> bool:
        return self._column_strings.str.contains(r"[a-z]", flags=re.IGNORECASE, regex=True).any()

    def _has_any_decimal_separator(self) -> bool:
        return self._column_strings.str.contains(REGEX_DECIMAL_SEPARATOR, flags=re.IGNORECASE, regex=True).any()


class _DecimalTypeDetector:
    def __init__(self, column_strings: Series):
        self._column_strings = column_strings

    def is_column_of_this_type(self) -> bool:
        column_numeric = _get_column_as_numeric(self._column_strings)
        if column_numeric is None:
            return False
        else:
            return column_numeric.dtype == "float64"


def _is_numeric_column(column: Series) -> bool:
    return _get_column_as_numeric(column) is not None


# TODO rm and work only with _is_numeric_column?
def _get_column_as_numeric(column: Series) -> tp.Optional[Series]:
    try:
        return pd.to_numeric(column, errors="raise")
    except ValueError:
        return None


# TODO rm
def print_df(df):
    pd.set_option("display.max_columns", None)
    print(df)
