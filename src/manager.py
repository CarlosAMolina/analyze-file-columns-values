import pandas as pd
import typing as tp

from src import extractors
from src import type_analyzer
from src import value_analyzer


def get_column_names_and_types_from_df(file_df: pd.DataFrame) -> tp.Dict[str, str]:
    result = {}
    for column_name, column_rows in file_df.items():
        print(column_name)  # TODO rm
        print(column_rows)  # TODO rm
        result[column_name] = type_analyzer.get_column_type(column_rows)
    print(result)  # TODO rm
    return result
