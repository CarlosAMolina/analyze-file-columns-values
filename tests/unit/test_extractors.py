import pathlib
import unittest

from pandas import DataFrame as Df
import pandas as pd
import numpy as np

from src import extractors


class TestFileIsReadAsExpected(unittest.TestCase):
    def test_decimal_column(self):
        column_name = "value"
        result = get_df_from_csv_test_file("all_possible_decimal_values.csv")[column_name]
        expected_result = pd.Series(
            data=["3.4", " 12345.12340", " 1.234512340e4", "3", np.nan, "-12345.1"], name=column_name
        )
        pd.testing.assert_series_equal(expected_result, result)

    def test_integer_column(self):
        column_name = "value"
        result = get_df_from_csv_test_file("all_possible_integer_values.csv")[column_name]
        expected_result = pd.Series(data=["1234", " 2", np.nan, "-3"], name=column_name)
        pd.testing.assert_series_equal(expected_result, result)

    def test_string_column(self):
        column_name = "value"
        result = get_df_from_csv_test_file("all_possible_string_values.csv")[column_name]
        expected_result = pd.Series(data=[" a", "b ", np.nan, " c ", " a b  ", " "], name=column_name)
        pd.testing.assert_series_equal(expected_result, result)


def get_df_from_csv_test_file(file_name: str) -> Df:
    script_dir = pathlib.Path(__file__).parent.absolute()
    tests_dir = script_dir.parent
    csv_file_path_name = str(pathlib.PurePath(tests_dir, "files", file_name))
    return extractors.get_df_from_csv(csv_file_path_name)
