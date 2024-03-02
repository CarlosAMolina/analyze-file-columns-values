import re
import typing as tp

import pandas as pd


def is_integer(column_strings: pd.Series):
    return _IntegerTypeAnalyzer(column_strings).is_column_of_this_type()


def is_decimal(column_strings: pd.Series):
    return _DecimalTypeAnalyzer(column_strings).is_column_of_this_type()


REGEX_DECIMAL_SEPARATOR = r"\."


class _IntegerTypeAnalyzer:
    def __init__(self, column_strings: "pd.Series[str]"):
        self._column_strings = column_strings

    def is_column_of_this_type(self) -> bool:
        if _is_numeric_column(self._column_strings) is False:
            return False
        elif self._has_any_decimal_separator():
            return False
        elif _has_column_any_character(self._column_strings):
            if _are_all_characters_e(self._column_strings):
                return _has_numeric_column_with_e_numbers_only_int_numbers(self._column_strings)
            else:
                return False
        return True

    def _has_any_decimal_separator(self) -> bool:
        return self._column_strings.str.contains(REGEX_DECIMAL_SEPARATOR, flags=re.IGNORECASE, regex=True).any()


class _DecimalTypeAnalyzer:
    def __init__(self, column_strings: "pd.Series[str]"):
        self._column_strings = column_strings

    def is_column_of_this_type(self) -> bool:
        column_numeric = _get_column_as_numeric(self._column_strings)
        if column_numeric is None:
            return False
        elif _has_column_any_character(self._column_strings):
            if _are_all_characters_e(self._column_strings):
                return not _has_numeric_column_with_e_numbers_only_int_numbers(self._column_strings)
            else:
                return False
        else:
            return column_numeric.dtype == "float64"


def _has_column_any_character(column: "pd.Series[str]") -> bool:
    return _has_row_any_character(column).any()


def _has_row_any_character(column: "pd.Series[str]") -> "pd.Series[bool]":
    return column.str.contains(r"[a-z]", flags=re.IGNORECASE, regex=True)


def _are_all_characters_e(column: "pd.Series[str]") -> bool:
    rows_with_characters = column[_has_row_any_character(column)]
    return not rows_with_characters.str.contains(r"[a-d]|[f-z]", flags=re.IGNORECASE, regex=True).all()


def _has_numeric_column_with_e_numbers_only_int_numbers(column: "pd.Series[str]") -> bool:
    column_numeric = _get_column_as_numeric(column)
    column_numeric_str = column_numeric.astype(str)
    decimal_values: pd.Series[str] = column_numeric_str.str.split(pat=".", expand=True)[1]
    # Convert to numeric an integer adds `.0`.
    return (decimal_values == "0").all()


def _is_numeric_column(column: pd.Series) -> bool:
    return _get_column_as_numeric(column) is not None


# TODO rm and work only with _is_numeric_column?
def _get_column_as_numeric(column: pd.Series) -> tp.Optional[pd.Series]:
    # TODO. Conflict with the logic when analyzing the column values because
    # withe spaces are not tripped when reading the csv file
    column_stripped = column.str.strip()
    try:
        return pd.to_numeric(column_stripped, errors="raise")
    except ValueError:
        return None


# TODO rm
def print_df(df):
    pd.set_option("display.max_columns", None)
    print(df)
