import pathlib
import unittest

from pandas import DataFrame as Df
import numpy as np

from src import file_manager
from src import value_analyzer


class TestAnalyzerClassesReadFromFile(unittest.TestCase):
    def setUp(self):
        self.df = get_df_from_csv_test_file("file.csv")

    def test_string_column_if_null_values(self):
        column_name = "Column string"
        column = self.df[column_name]
        analysis = value_analyzer.StringColumnAnalyzer(column)
        self.assertTrue(analysis.has_null_values())
        self.assertFalse(analysis.has_empty_values_if_no_stripped())
        self.assertTrue(analysis.has_empty_values_if_stripped())
        self.assertEqual(7, analysis.max_length_if_stripped())
        self.assertEqual(9, analysis.max_length_if_no_stripped())
        self.assertEqual(0, analysis.min_length_if_stripped())
        self.assertEqual(1, analysis.min_length_if_no_stripped())
        self.assertEqual(["Foo Bar", "Bar Foo"], analysis.max_values_if_stripped())
        self.assertEqual([" Foo Bar "], analysis.max_values_if_no_stripped())
        self.assertEqual([""], analysis.min_values_if_stripped())
        self.assertEqual([" "], analysis.min_values_if_no_stripped())

    def test_string_column_if_no_null_values(self):
        column_name = "Column string all lines with value"
        column = self.df[column_name]
        analysis = value_analyzer.StringColumnAnalyzer(column)
        self.assertFalse(analysis.has_null_values())

    def test_integer_column(self):
        column_name = "Column integer"
        column = self.df[column_name]
        analysis = value_analyzer.IntegerColumnAnalyzer(column)
        self.assertTrue(analysis.has_null_values())
        self.assertEqual(1111, analysis.max_value())
        self.assertEqual(np.int64, type(analysis.max_value()))
        self.assertEqual(1, analysis.min_value())
        self.assertEqual(np.int64, type(analysis.min_value()))
        self.assertEqual(4, analysis.max_length())
        self.assertEqual(np.int64, type(analysis.max_length()))
        self.assertEqual(1, analysis.min_length())
        self.assertEqual(np.int64, type(analysis.min_length()))

    def test_decimal_column(self):
        column_name = "Column decimal"
        column = self.df[column_name]
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertTrue(analysis.has_null_values())
        # Check trailing 0 is not deleted
        self.assertEqual(" 12345.12340", analysis.max_value())
        self.assertEqual("-12345.1", analysis.min_value())
        self.assertEqual(np.int64, type(analysis.max_length_of_integer_part()))
        self.assertEqual(5, analysis.max_length_of_integer_part())
        self.assertEqual(
            [" 12345.12340", " 1.234512340e4", "-12345.1"], analysis.values_with_max_length_of_integer_part()
        )
        self.assertEqual(np.int64, type(analysis.max_length_of_decimal_part()))
        self.assertEqual(5, analysis.max_length_of_decimal_part())
        self.assertEqual([" 12345.12340", " 1.234512340e4"], analysis.values_with_max_length_of_decimal_part())


def get_df_from_csv_test_file(file_name: str) -> Df:
    script_dir = pathlib.Path(__file__).parent.absolute()
    tests_dir = script_dir.parent
    csv_file_path_name = str(pathlib.PurePath(tests_dir, "files", file_name))
    return file_manager.get_df_from_csv(csv_file_path_name)
