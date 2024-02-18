import decimal
import typing as tp

from pandas import DataFrame as Df
from pandas import Series
import pandas as pd


def get_df_from_csv(path_name: str):
    # Read all columns as str to not modify numeric values
    return pd.read_csv(path_name, dtype=str)


def show_decimal_column_analysis(column: Series):
    print()
    print(f"Analyzed decimal column: {column.name}")
    analysis = DecimalColumnAnalyzer(column)
    print("Are there null values?", analysis.has_null_values())
    print("Maximum results:")
    print("  Maximum value:", analysis.max_value())
    print(
        "  Integer part. Maximum number of digits: {}. Values: {}".format(
            analysis.max_length_of_integer_part(),
            analysis.values_with_max_length_of_integer_part(),
        )
    )
    print(
        "  Decimal part. Maximum number of digits: {}. Values: {}".format(
            analysis.max_length_of_decimal_part(),
            analysis.values_with_max_length_of_decimal_part(),
        )
    )
    print("Minimum value:", analysis.min_value())


def show_integer_column_analysis(column: Series):
    print()
    print(f"Analyzed integer column: {column.name}")
    analysis = IntegerColumnAnalyzer(column)
    print("Are there null values?", analysis.has_null_values())
    print(
        "Max value. Number of digits: {}. Value: {}".format(
            analysis.max_length(),
            analysis.max_value(),
        )
    )
    print(
        "Min value. Number of digits: {}. Value: {}".format(
            analysis.min_length(),
            analysis.min_value(),
        )
    )


def show_string_column_analysis(column: Series):
    print()
    print(f"Analyzed string column: {column.name}")
    analysis = StringColumnAnalyzer(column)
    print("Are there null values?", analysis.has_null_values())
    print("Are there empty values?")
    print("  If values are stripped:", analysis.has_empty_values_if_stripped())
    print("  If values are not stripped:", analysis.has_empty_values_if_no_stripped())
    print("Values with maximum length:")
    print(
        "  If values are stripped. Number of characters: {}. Values: {}".format(
            analysis.max_length_if_stripped(),
            analysis.max_values_if_stripped(),
        )
    )
    print(
        "  If values are not stripped. Number of characters: {}. Values: {}".format(
            analysis.max_length_if_no_stripped(),
            analysis.max_values_if_no_stripped(),
        )
    )
    print("Values with minimum length:")
    print(
        "  If values are stripped. Number of characters: {}. Values: {}".format(
            analysis.min_length_if_stripped(),
            analysis.min_values_if_stripped(),
        )
    )
    print(
        "  If values are not stripped. Number of characters: {}. Values: {}".format(
            analysis.min_length_if_no_stripped(),
            analysis.min_values_if_no_stripped(),
        )
    )


class StringColumnAnalyzer:
    def __init__(self, column: Series):
        self._column = column
        self._df_to_analyze = None  # Never call this, work with `self._df`

    def has_null_values(self) -> bool:
        return self._column.isnull().values.any()

    def has_empty_values_if_stripped(self) -> bool:
        df = self._get_df_add_analysis_columns()
        condition = df[f"{self._column_name_stripped}_length"] == 0
        return condition.any()

    def has_empty_values_if_no_stripped(self) -> bool:
        condition = self._df[f"{self._column_name}_length"] == 0
        return condition.any()

    def max_length_if_stripped(self) -> int:
        return self._df[f"{self._column_name_stripped}_length"].max()

    def max_length_if_no_stripped(self) -> int:
        return self._df[f"{self._column_name}_length"].max()

    def min_length_if_stripped(self) -> int:
        return self._df[f"{self._column_name_stripped}_length"].min()

    def min_length_if_no_stripped(self) -> int:
        return self._df[f"{self._column_name}_length"].min()

    def max_values_if_stripped(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name_stripped}_length"] == self.max_length_if_stripped()
        column_name = self._column_name_stripped
        return get_unique_values_of_column(column_name, condition, self._df)

    def max_values_if_no_stripped(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name}_length"] == self.max_length_if_no_stripped()
        column_name = self._column_name
        return get_unique_values_of_column(column_name, condition, self._df)

    def min_values_if_stripped(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name_stripped}_length"] == self.min_length_if_stripped()
        column_name = self._column_name_stripped
        return get_unique_values_of_column(column_name, condition, self._df)

    def min_values_if_no_stripped(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name}_length"] == self.min_length_if_no_stripped()
        column_name = self._column_name
        return get_unique_values_of_column(column_name, condition, self._df)

    @property
    def _df(self) -> Df:
        if self._df_to_analyze is None:
            self._df_to_analyze = self._get_df_add_analysis_columns()
        return self._df_to_analyze

    def _get_df_add_analysis_columns(self) -> Df:
        result = Df(self._column)
        result[f"{self._column_name}_length"] = result[self._column.name].str.len().astype("Int64")
        result[f"{self._column_name_stripped}"] = result[self._column.name].str.strip()
        result[f"{self._column_name_stripped}_length"] = result[self._column_name_stripped].str.len().astype("Int64")
        return result

    @property
    def _column_name_stripped(self) -> str:
        return f"{self._column.name}_stripped"

    @property
    def _column_name(self) -> str:
        return self._column.name


def get_unique_values_of_column(
    column_name: str,
    condition: Series,
    df: Df,
) -> tp.List[tp.Any]:
    return df.loc[condition][column_name].drop_duplicates().to_list()


class IntegerColumnAnalyzer:
    def __init__(self, column: Series):
        self._column = column
        self._df_to_analyze = None  # Never call this, work with `self._df`

    def has_null_values(self) -> bool:
        return self._column.isnull().values.any()

    def max_value(self) -> int:
        return self._df[f"{self._column_name}_int"].max()

    def min_value(self) -> int:
        return self._df[f"{self._column_name}_int"].min()

    def max_length(self) -> int:
        return self._df[f"{self._column_name}_length"].max()

    def min_length(self) -> int:
        return self._df[f"{self._column_name}_length"].min()

    @property
    def _df(self) -> Df:
        if self._df_to_analyze is None:
            self._df_to_analyze = self._get_df_add_analysis_columns()
        return self._df_to_analyze

    def _get_df_add_analysis_columns(self) -> Df:
        result = Df(self._column)
        result[f"{self._column_name}_int"] = result[self._column.name].astype("Int64")
        result[f"{self._column_name}_int_absolute"] = result[f"{self._column_name}_int"].abs()
        result.loc[~result[self._column.name].isnull(), f"{self._column_name}_length"] = (
            result[f"{self._column_name}_int_absolute"].astype(str).str.len()
        )
        result[f"{self._column_name}_length"] = result[f"{self._column_name}_length"].astype("Int64")
        return result

    @property
    def _column_name(self) -> str:
        return self._column.name


class DecimalColumnAnalyzer:
    def __init__(self, column: Series):
        self._column = column
        self._df_to_analyze = None  # Never call this, work with `self._df`

    def has_null_values(self) -> bool:
        return self._column.isnull().values.any()

    def max_value(self) -> str:
        return self._df.loc[
            self._df[f"{self._column_name}_numeric"] == self._df[f"{self._column_name}_numeric"].max(),
            self._column_name,
        ].iloc[0]

    def min_value(self) -> str:
        return self._df.loc[
            self._df[f"{self._column_name}_numeric"] == self._df[f"{self._column_name}_numeric"].min(),
            self._column_name,
        ].iloc[0]

    def max_length_of_integer_part(self) -> int:
        return self._df[f"{self._column_name}_int_length"].max()

    def max_length_of_decimal_part(self) -> int:
        return self._df[f"{self._column_name}_decimal_length"].max()

    def values_with_max_length_of_integer_part(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name}_int_length"] == self.max_length_of_integer_part()
        return get_unique_values_of_column(self._column_name, condition, self._df)

    def values_with_max_length_of_decimal_part(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name}_decimal_length"] == self.max_length_of_decimal_part()
        return get_unique_values_of_column(self._column_name, condition, self._df)

    @property
    def _df(self) -> Df:
        if self._df_to_analyze is None:
            self._df_to_analyze = self._get_df_add_analysis_columns()
        return self._df_to_analyze

    def _get_df_add_analysis_columns(self) -> Df:
        # TODO manage if string column with different millar and decimal sepparator signs
        result = Df(self._column)
        result[f"{self._column_name}_numeric"] = [decimal.Decimal(value) for value in result[self._column_name]]
        result[f"{self._column_name}_numeric_str"] = [
            "{:f}".format(value) for value in result[f"{self._column_name}_numeric"]
        ]
        condition_is_null = result[self._column_name].isnull()
        result[f"{self._column_name}_int"] = (
            result.loc[~condition_is_null, f"{self._column_name}_numeric_str"].str.split(".").str[0].astype("Int64")
        )
        result[f"{self._column_name}_int_absolute"] = result[f"{self._column_name}_int"].abs()
        result[f"{self._column_name}_decimal"] = (
            result.loc[~condition_is_null, f"{self._column_name}_numeric_str"].str.split(".").str[1].astype("Int64")
        )
        result[f"{self._column_name}_int_length"] = (
            result.loc[~result[f"{self._column_name}_int_absolute"].isnull(), f"{self._column_name}_int_absolute"]
            .astype(str)
            .str.len()
            .astype("Int64")
        )
        result[f"{self._column_name}_decimal_length"] = (
            result.loc[~result[f"{self._column_name}_decimal"].isnull(), f"{self._column_name}_decimal"]
            .astype(str)
            .str.len()
            .astype("Int64")
        )
        result[f"{self._column_name}_decimal_length"] = result[f"{self._column_name}_decimal_length"].fillna(0)
        # print_df(result)
        return result

    @property
    def _column_name(self) -> str:
        return self._column.name


def print_df(df: Df):
    pd.set_option("display.max_columns", None)
    print(df)
