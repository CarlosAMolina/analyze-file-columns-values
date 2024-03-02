import re
import typing as tp

import pandas as pd


def is_integer(column_strings: pd.Series):
    return _IntegerTypeAnalyzer(column_strings).is_column_of_this_type()


def is_decimal(column_strings: pd.Series):
    return _DecimalTypeAnalyzer(column_strings).is_column_of_this_type()


REGEX_DECIMAL_SEPARATOR = r"\."


class _IntegerTypeAnalyzer:
    def __init__(self, column_strings: pd.Series):
        self._column_strings = column_strings

    def is_column_of_this_type(self) -> bool:
        if _is_numeric_column(self._column_strings) is False:
            return False
        elif self._has_any_decimal_separator():
            return False
        elif self._has_column_any_character():
            if self._are_all_characters_e():
                column_numeric = _get_column_as_numeric(self._column_strings)
                # Convert to numeric an integer adds `.0`.
                column_numeric_str = column_numeric.astype(str)
                print(column_numeric_str)
                decimal_values: pd.Series[str] = column_numeric_str.str.split(pat=".", expand=True)[1]
                return (decimal_values == "0").all()
            else:
                return False
        return True

    def _has_column_any_character(self) -> bool:
        return self._has_row_any_character().any()

    def _has_row_any_character(self) -> pd.Series:
        return self._column_strings.str.contains(r"[a-z]", flags=re.IGNORECASE, regex=True)

    def _has_any_decimal_separator(self) -> bool:
        return self._column_strings.str.contains(REGEX_DECIMAL_SEPARATOR, flags=re.IGNORECASE, regex=True).any()

    def _are_all_characters_e(self) -> bool:
        rows_with_characters = self._column_strings[self._has_row_any_character()]
        return not rows_with_characters.str.contains(r"[a-d]|[f-z]", flags=re.IGNORECASE, regex=True).all()


class _DecimalTypeAnalyzer:
    def __init__(self, column_strings: pd.Series):
        self._column_strings = column_strings

    def is_column_of_this_type(self) -> bool:
        column_numeric = _get_column_as_numeric(self._column_strings)
        if column_numeric is None:
            return False
        else:
            return column_numeric.dtype == "float64"


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
