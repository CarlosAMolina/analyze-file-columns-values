import decimal
import typing as tp

from pandas import DataFrame as Df
from pandas import Series


def _get_values_applying_limitacion(values: list) -> tp.Union[str, list]:
    MAX_VALUES_TO_SHOW = 4
    if len(values) > MAX_VALUES_TO_SHOW:
        values_to_show = values[:MAX_VALUES_TO_SHOW]
        values_to_show_str = str(values_to_show).replace("]", ", ...")
        return f"{values_to_show_str} (more values are omitted)"
    else:
        return values


class _StringBaseColumnAnalysis(tp.NamedTuple):
    has_empty_values: bool
    max_length: int
    min_length: int
    max_values: tp.List[str]
    min_values: tp.List[str]


class _StringColumnAnalysis(tp.NamedTuple):
    has_null_values: bool
    stripped: _StringBaseColumnAnalysis
    no_stripped: _StringBaseColumnAnalysis


ColumnValuesAnalysisSummary = str


# TODO rm
def show_string_column_analysis(analysis: _StringColumnAnalysis):
    print(get_string_column_analysis_summary(analysis))


def get_string_column_analysis_summary(analysis: _StringColumnAnalysis) -> ColumnValuesAnalysisSummary:
    result = "Are there null values? {}".format(analysis.has_null_values)
    result += "\nAre there empty values?"
    result += "\n  If values are stripped: {}".format(analysis.stripped.has_empty_values)
    result += "\n  If values are not stripped: {}".format(analysis.no_stripped.has_empty_values)
    result += "\nValues with maximum length:"
    max_values_if_stripped = analysis.stripped.max_values
    result += "\n  If values are stripped. Number of characters: {}. Values ({}): {}".format(
        analysis.stripped.max_length,
        len(max_values_if_stripped),
        _get_values_applying_limitacion(max_values_if_stripped),
    )
    max_values_if_no_stripped = analysis.no_stripped.max_values
    result += "\n  If values are not stripped. Number of characters: {}. Values ({}): {}".format(
        analysis.no_stripped.max_length,
        len(max_values_if_no_stripped),
        _get_values_applying_limitacion(max_values_if_no_stripped),
    )
    result += "\nValues with minimum length:"
    min_values_if_stripped = analysis.stripped.min_values
    result += "\n  If values are stripped. Number of characters: {}. Values ({}): {}".format(
        analysis.stripped.min_length,
        len(min_values_if_stripped),
        _get_values_applying_limitacion(min_values_if_stripped),
    )
    min_values_if_no_stripped = analysis.no_stripped.min_values
    result += "\n  If values are not stripped. Number of characters: {}. Values ({}): {}".format(
        analysis.no_stripped.min_length,
        len(min_values_if_no_stripped),
        _get_values_applying_limitacion(min_values_if_no_stripped),
    )
    return result


def get_string_analysis(column: Series) -> _StringColumnAnalysis:
    analysis = _StringColumnAnalyzer(column)
    stripped_analysis = _StringBaseColumnAnalysis(
        analysis.has_empty_values_if_stripped(),
        analysis.max_length_if_stripped(),
        analysis.min_length_if_stripped(),
        analysis.max_values_if_stripped(),
        analysis.min_values_if_stripped(),
    )
    no_stripped_analysis = _StringBaseColumnAnalysis(
        analysis.has_empty_values_if_no_stripped(),
        analysis.max_length_if_no_stripped(),
        analysis.min_length_if_no_stripped(),
        analysis.max_values_if_no_stripped(),
        analysis.min_values_if_no_stripped(),
    )
    return _StringColumnAnalysis(
        analysis.has_null_values(),
        stripped_analysis,
        no_stripped_analysis,
    )


SqlDefinition = str


def get_string_sql_definition(analysis: _StringColumnAnalysis, column_name: str) -> SqlDefinition:
    return "{} varchar({}) {},".format(
        column_name, analysis.no_stripped.max_length, _get_null_sql_definition(analysis.has_null_values)
    )


def _get_null_sql_definition(has_null_values: bool) -> str:
    return "NULL" if has_null_values else "NOT NULL"


class _StringColumnAnalyzer:
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
        return _get_unique_values_of_column(column_name, condition, self._df)

    def max_values_if_no_stripped(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name}_length"] == self.max_length_if_no_stripped()
        column_name = self._column_name
        return _get_unique_values_of_column(column_name, condition, self._df)

    def min_values_if_stripped(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name_stripped}_length"] == self.min_length_if_stripped()
        column_name = self._column_name_stripped
        return _get_unique_values_of_column(column_name, condition, self._df)

    def min_values_if_no_stripped(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name}_length"] == self.min_length_if_no_stripped()
        column_name = self._column_name
        return _get_unique_values_of_column(column_name, condition, self._df)

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


def _get_unique_values_of_column(
    column_name: str,
    condition: Series,
    df: Df,
) -> tp.List[tp.Any]:
    return df.loc[condition][column_name].drop_duplicates().to_list()


class _IntegerColumnAnalysis(tp.NamedTuple):
    has_null_values: bool
    max_length: int
    min_length: int
    max_value: int
    min_value: int


# TODO rm
def show_integer_column_analysis(analysis: _IntegerColumnAnalysis):
    print(get_integer_column_analysis_summary(analysis))


def get_integer_column_analysis_summary(analysis: _IntegerColumnAnalysis) -> ColumnValuesAnalysisSummary:
    result = "Are there null values? {}".format(analysis.has_null_values)
    result += "\nMax value. Number of digits: {}. Value: {}".format(
        analysis.max_length,
        analysis.max_value,
    )
    result += "\nMin value. Number of digits: {}. Value: {}".format(
        analysis.min_length,
        analysis.min_value,
    )
    return result


def get_integer_analysis(column: Series) -> _IntegerColumnAnalysis:
    analysis = _IntegerColumnAnalyzer(column)
    return _IntegerColumnAnalysis(
        analysis.has_null_values(),
        analysis.max_length(),
        analysis.min_length(),
        analysis.max_value(),
        analysis.min_value(),
    )


def get_integer_sql_definition(analysis: _IntegerColumnAnalysis, column_name: str) -> SqlDefinition:
    # https://dev.mysql.com/doc/refman/8.0/en/integer-types.html
    mysql_definition_max_value = {
        "integer": 2147483647,
    }
    null_definition = _get_null_sql_definition(analysis.has_null_values)
    # TODO check min value too to recommend unsigned
    definition = "bigint"
    if analysis.max_length < len(str(mysql_definition_max_value["integer"])):
        definition = "integer"
    return "{} {} {},".format(column_name, definition, null_definition)


class _IntegerColumnAnalyzer:
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


# TODO rm
def show_all_null_column_analysis():
    print(get_all_null_column_analysis_summary())


_NOT_ENOUGHT_INFORMATION_TEXT = "not enough information to analyze because all values are null"


def get_all_null_column_analysis_summary() -> ColumnValuesAnalysisSummary:
    return f"All values are null ({_NOT_ENOUGHT_INFORMATION_TEXT})"


def get_all_null_sql_definition(column_name: str) -> SqlDefinition:
    return "{} {} ({})".format(
        column_name,
        _get_null_sql_definition(has_null_values=True),
        _NOT_ENOUGHT_INFORMATION_TEXT,
    )


class _DecimalColumnAnalysis(tp.NamedTuple):
    has_null_values: bool
    max_value: str
    min_value: str
    max_length_of_integer_part: int
    max_length_of_decimal_part: int
    values_with_max_length_of_integer_part: tp.List[str]
    values_with_max_length_of_decimal_part: tp.List[str]


# TODO rm
def show_decimal_column_analysis(analysis: _DecimalColumnAnalysis):
    print(get_decimal_column_analysis_summary(analysis))


def get_decimal_column_analysis_summary(analysis: _DecimalColumnAnalysis) -> ColumnValuesAnalysisSummary:
    result = "Are there null values? {}".format(analysis.has_null_values)
    result += "\nMaximum results:"
    result += "\n  Maximum value: {}".format(analysis.max_value)
    values_with_max_length_of_integer_part = analysis.values_with_max_length_of_integer_part
    result += "\n  Integer part. Maximum number of digits: {}. Values ({}): {}".format(
        analysis.max_length_of_integer_part,
        len(values_with_max_length_of_integer_part),
        _get_values_applying_limitacion(values_with_max_length_of_integer_part),
    )
    values_with_max_length_of_decimal_part = analysis.values_with_max_length_of_decimal_part
    result += "\n  Decimal part. Maximum number of digits: {}. Values ({}): {}".format(
        analysis.max_length_of_decimal_part,
        len(values_with_max_length_of_decimal_part),
        _get_values_applying_limitacion(values_with_max_length_of_decimal_part),
    )
    result += "\nMinimum value: {}".format(analysis.min_value)
    return result


def get_decimal_analysis(column: Series) -> _DecimalColumnAnalysis:
    analysis = _DecimalColumnAnalyzer(column)
    return _DecimalColumnAnalysis(
        analysis.has_null_values(),
        analysis.max_value(),
        analysis.min_value(),
        analysis.max_length_of_integer_part(),
        analysis.max_length_of_decimal_part(),
        analysis.values_with_max_length_of_integer_part(),
        analysis.values_with_max_length_of_decimal_part(),
    )


def get_decimal_sql_definition(analysis: _DecimalColumnAnalysis, column_name: str) -> SqlDefinition:
    null_definition = _get_null_sql_definition(analysis.has_null_values)
    return "{} decimal({},{}) {},".format(
        column_name,
        analysis.max_length_of_integer_part + analysis.max_length_of_decimal_part,
        analysis.max_length_of_decimal_part,
        null_definition,
    )


class _DecimalColumnAnalyzer:
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
        return _get_unique_values_of_column(self._column_name, condition, self._df)

    def values_with_max_length_of_decimal_part(self) -> tp.List[str]:
        condition = self._df[f"{self._column_name}_decimal_length"] == self.max_length_of_decimal_part()
        return _get_unique_values_of_column(self._column_name, condition, self._df)

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
        return result

    @property
    def _column_name(self) -> str:
        return self._column.name
