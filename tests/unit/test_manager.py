import pathlib
import unittest

from pandas import DataFrame as Df

from src import extractors
from src import manager
from src import type_analyzer


class TestFunction_show_file_analysis(unittest.TestCase):
    def test_does_not_raise_exception(self):
        file_path_name = get_test_file_path_name("file.csv")
        manager.show_file_analysis(file_path_name)


class TestFunction_get_column_names_and_types_from_df(unittest.TestCase):
    def test_expected_result_is_returned(self):
        file_df = get_df_from_csv_test_file("file.csv")
        result = [
            (column_name, type_analyzer.get_column_type(column_series))
            for column_name, column_series in file_df.items()
        ]
        expected_result = [
            ("Column string", type_analyzer.Type.STRING),
            ("Column string all lines with value", type_analyzer.Type.STRING),
            ("Column integer", type_analyzer.Type.INTEGER),
            ("Column decimal", type_analyzer.Type.DECIMAL),
        ]
        self.assertEqual(result, expected_result)


def get_df_from_csv_test_file(file_name: str) -> Df:
    csv_file_path_name = get_test_file_path_name(file_name)
    return extractors.get_df_from_csv(csv_file_path_name)


def get_test_file_path_name(file_name: str) -> str:
    script_dir = pathlib.Path(__file__).parent.absolute()
    tests_dir = script_dir.parent
    return str(pathlib.PurePath(tests_dir, "files", file_name))
