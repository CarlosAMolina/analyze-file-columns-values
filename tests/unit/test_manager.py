import pathlib
import unittest

from pandas import DataFrame as Df

from src import extractors
from src import manager
from src import type_analyzer


class TestFunction_get_column_names_and_types_from_df(unittest.TestCase):
    def test_expected_result_is_returned(self):
        df = get_df_from_csv_test_file("file.csv")
        result = manager._get_column_names_and_types_from_df(df)
        expected_result = {
            "Column string": type_analyzer.Type.STRING,
            "Column string all lines with value": type_analyzer.Type.STRING,
            "Column integer": type_analyzer.Type.INTEGER,
            "Column decimal": type_analyzer.Type.DECIMAL,
        }
        self.assertEqual(result, expected_result)


def get_df_from_csv_test_file(file_name: str) -> Df:
    script_dir = pathlib.Path(__file__).parent.absolute()
    tests_dir = script_dir.parent
    csv_file_path_name = str(pathlib.PurePath(tests_dir, "files", file_name))
    return extractors.get_df_from_csv(csv_file_path_name)
