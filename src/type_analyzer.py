import re
import typing as tp
import enum

import pandas as pd


class Type(enum.Enum):
    INTEGER = "integer"
    DECIMAL = "decimal"
    STRING = "string"


def get_column_type(column: "pd.Series[str]") -> Type:
    if _IntegerTypeAnalyzer(column).is_column_of_this_type():
        return Type.INTEGER
    elif _DecimalTypeAnalyzer(column).is_column_of_this_type():
        return Type.DECIMAL
    else:
        return Type.STRING


class _IntegerTypeAnalyzer:
    def __init__(self, column_strings: "pd.Series[str]"):
        self._column_strings = column_strings

    def is_column_of_this_type(self) -> bool:
        column_numeric = _get_column_as_numeric(self._column_strings)
        if column_numeric is None:
            return False
        # TODO maybe int numbers has thousand separator
        elif self._has_any_decimal_separator():
            return False
        elif _has_column_any_character(self._column_strings):
            if _are_all_characters_e(self._column_strings):
                return _has_numeric_column_of_e_numbers_only_int_numbers(column_numeric)
            else:
                return False
        return True

    def _has_any_decimal_separator(self) -> bool:
        REGEX_DECIMAL_SEPARATOR = r"\."
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
                return not _has_numeric_column_of_e_numbers_only_int_numbers(column_numeric)
            else:
                return False
        else:
            return column_numeric.dtype == "float64"


def _has_column_any_character(column: "pd.Series[str]") -> bool:
    return _has_row_any_character(column).any()


def _has_row_any_character(column: "pd.Series[str]") -> "pd.Series[bool]":
    result = column.str.contains(r"[a-z]", flags=re.IGNORECASE, regex=True)
    result = result.fillna(False)
    return result


def _are_all_characters_e(column: "pd.Series[str]") -> bool:
    rows_with_characters = column[_has_row_any_character(column)]
    return not rows_with_characters.str.contains(r"[a-d]|[f-z]", flags=re.IGNORECASE, regex=True).all()


def _has_numeric_column_of_e_numbers_only_int_numbers(column: "pd.Series[int|float]") -> bool:
    column_str = column.astype(str)
    decimal_values: pd.Series[str] = column_str.str.split(pat=".", expand=True)[1]
    # Convert to numeric an integer adds `.0`.
    return (decimal_values == "0").all()


def _get_column_as_numeric(column: pd.Series) -> tp.Optional[pd.Series]:
    # TODO. Conflict with the logic when analyzing the column values because
    # withe spaces are not tripped when reading the csv file
    column_stripped = column.str.strip()
    try:
        return pd.to_numeric(column_stripped, errors="raise")
    except ValueError:
        return None
