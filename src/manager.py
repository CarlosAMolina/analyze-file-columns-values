import pandas as pd
import typing as tp

from src import extractors
from src import type_analyzer


def show_file_analysis(file_path_name: str):
    file_df = extractors.get_df_from_csv(file_path_name)
    for column_name, column_type in _get_column_names_and_types_from_df(file_df):
        print(column_name, column_type)  # TODO rm


def _get_column_names_and_types_from_df(file_df: pd.DataFrame) -> tp.Iterator[tp.Tuple[str, str]]:
    for column_name, column_rows in file_df.items():
        yield column_name, type_analyzer.get_column_type(column_rows)
