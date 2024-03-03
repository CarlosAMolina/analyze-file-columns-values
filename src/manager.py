import pandas as pd
import typing as tp

from src import type_analyzer


def _get_column_names_and_types_from_df(file_df: pd.DataFrame) -> tp.Dict[str, str]:
    return {column_name: type_analyzer.get_column_type(column_rows) for column_name, column_rows in file_df.items()}
