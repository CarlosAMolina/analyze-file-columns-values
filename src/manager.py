import datetime
import typing as tp

from pandas import Series
from pandas import DataFrame as Df

from src import extractors
from src import type_analyzer
from src import value_analyzer


def show_file_analysis(file_path_name: str):
    print("[{}] Analyzing file {}".format(datetime.datetime.now(), file_path_name))
    file_df = extractors.get_df_from_csv(file_path_name)
    column_names = file_df.columns.tolist()
    sql_definition: tp.List[str] = []
    for index, analysis in enumerate(_get_columns_analysis(file_df), 1):
        print()
        print(
            "[{}] Analyzing column {} of {}. Column name: {}".format(
                datetime.datetime.now(),
                index,
                len(column_names),
                analysis.column_name,
            )
        )
        print(f"Column type: {analysis.column_type.value}")
        print(analysis.summary)
        sql_definition.append(analysis.sql_definition)
    _show_sql_definition(sql_definition)


_ColumnAnalysisResults = tp.Tuple[value_analyzer.ColumnValuesAnalysisSummary, value_analyzer.SqlDefinition]


class _ColumnAnalysis(tp.NamedTuple):
    column_name: str
    column_type: type_analyzer.Type
    summary: value_analyzer.ColumnValuesAnalysisSummary
    sql_definition: value_analyzer.SqlDefinition


def _get_columns_analysis(df: Df) -> tp.Iterator[_ColumnAnalysis]:
    for column_name in df:
        column = df[column_name]
        column_type = type_analyzer.get_column_type(column)
        if column_type == type_analyzer.Type.ALL_NULL:
            analysis_summary = value_analyzer.get_all_null_column_analysis_summary()
            sql_definition = value_analyzer.get_all_null_sql_definition(column_name)
        elif column_type == type_analyzer.Type.DECIMAL:
            analysis_summary, sql_definition = _get_decimal_analysis(column, column_name)
        elif column_type == type_analyzer.Type.INTEGER:
            analysis_summary, sql_definition = _get_integer_analysis(column, column_name)
        elif column_type == type_analyzer.Type.STRING:
            analysis_summary, sql_definition = _get_string_analysis(column, column_name)
        else:
            raise ValueError(column_type)
        yield _ColumnAnalysis(column_name, column_type, analysis_summary, sql_definition)


def _get_decimal_analysis(column: Series, column_name: str) -> _ColumnAnalysisResults:
    analysis = value_analyzer.get_decimal_analysis(column)
    analysis_summary = value_analyzer.get_decimal_column_analysis_summary(analysis)
    sql_definition = value_analyzer.get_decimal_sql_definition(analysis, column_name)
    return analysis_summary, sql_definition


def _get_integer_analysis(column: Series, column_name: str) -> _ColumnAnalysisResults:
    analysis = value_analyzer.get_integer_analysis(column)
    analysis_summary = value_analyzer.get_integer_column_analysis_summary(analysis)
    sql_definition = value_analyzer.get_integer_sql_definition(analysis, column_name)
    return analysis_summary, sql_definition


def _get_string_analysis(column: Series, column_name: str) -> _ColumnAnalysisResults:
    analysis = value_analyzer.get_string_analysis(column)
    analysis_summary = value_analyzer.get_string_column_analysis_summary(analysis)
    sql_definition = value_analyzer.get_string_sql_definition(analysis, column_name)
    return analysis_summary, sql_definition


def _show_sql_definition(sql_definition: tp.List[str]):
    print("\nSQL definition")
    sql_definition_str = "\n".join(sql_definition)
    print(sql_definition_str)
