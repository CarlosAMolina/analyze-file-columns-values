import pandas as pd
import typing as tp

from src import extractors
from src import type_analyzer


def show_file_analisis(file_path_name: str) -> tp.Dict[str, str]:
    file_df = extractors.get_df_from_csv(file_path_name)
    for column_name, column_type in _get_column_names_and_types_from_df(file_df).items():
        print(column_name, column_type)  # TODO rm


def _get_column_names_and_types_from_df(file_df: pd.DataFrame) -> tp.Dict[str, str]:
    return {column_name: type_analyzer.get_column_type(column_rows) for column_name, column_rows in file_df.items()}
