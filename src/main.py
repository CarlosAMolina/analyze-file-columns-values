from pandas import DataFrame as Df
from pandas import Series
import pandas as pd


def get_df_from_csv(path_name: str):
    return pd.read_csv(path_name)


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
        result[f"{self._column_name}_int"] = result[self._column.name].astype('Int64')
        result[f"{self._column_name}_length"] = result[f"{self._column_name}_int"].astype(str).str.len()
        result.loc[
                result[self._column.name].isnull(),
                f"{self._column_name}_length"] = None
        result[f"{self._column_name}_length"] = result[f"{self._column_name}_length"].astype('Int64')
        return result

    @property
    def _column_name(self) -> str:
        return self._column.name
