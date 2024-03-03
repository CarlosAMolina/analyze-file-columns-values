import pandas as pd
import typing as tp

from src import extractors
from src import type_analyzer
from src import value_analyzer


def show_file_analysis(file_path_name: str):
    file_df = extractors.get_df_from_csv(file_path_name)
    for column_name in file_df:
        column = file_df[column_name]
        column_type = type_analyzer.get_column_type(column)
        if column_type == type_analyzer.Type.DECIMAL:
            value_analyzer.show_decimal_column_analysis(column)
        elif column_type == type_analyzer.Type.INTEGER:
            value_analyzer.show_integer_column_analysis(column)
        elif column_type == type_analyzer.Type.STRING:
            value_analyzer.show_string_column_analysis(column)
        else:
            raise ValueError(column_type)


# TODO rm
def _get_column_names_and_types_from_df(file_df: pd.DataFrame) -> tp.Iterator[tp.Tuple[str, str]]:
    for column_name, column_rows in file_df.items():
        yield column_name, type_analyzer.get_column_type(column_rows)
