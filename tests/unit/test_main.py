import pathlib
import unittest

import numpy as np

from src import main


class TestStringColumnAnalyzer(unittest.TestCase):
    def setUp(self):
        script_dir = pathlib.Path(__file__).parent.absolute()
        tests_dir = script_dir.parent
        csv_file_path_name = str(pathlib.PurePath(tests_dir, "files", "file.csv"))
        self.df = main.get_df_from_csv(csv_file_path_name)

    def test_string_column_if_null_values(self):
        column_name = "Column string"
        column = self.df[column_name]
        analisis = main.StringColumnAnalyzer(column)
        self.assertTrue(analisis.has_null_values())
        self.assertFalse(analisis.has_empty_values_if_no_stripped())
        self.assertTrue(analisis.has_empty_values_if_stripped())
        self.assertEqual(7, analisis.max_length_if_stripped())
        self.assertEqual(9, analisis.max_length_if_no_stripped())
        self.assertEqual(0, analisis.min_length_if_stripped())
        self.assertEqual(1, analisis.min_length_if_no_stripped())
        self.assertEqual(1, analisis.min_length_if_no_stripped())
        self.assertEqual(["Foo Bar", "Bar Foo"], analisis.max_values_if_stripped())
        self.assertEqual([" Foo Bar "], analisis.max_values_if_no_stripped())
        self.assertEqual([""], analisis.min_values_if_stripped())
        self.assertEqual([" "], analisis.min_values_if_no_stripped())

    def test_string_column_if_no_null_values(self):
        column_name = "Column string all lines with value"
        column = self.df[column_name]
        analisis = main.StringColumnAnalyzer(column)
        self.assertFalse(analisis.has_null_values())

    def test_integer_column(self):
        column_name = "Column integer"
        column = self.df[column_name]
        analisis = main.IntegerColumnAnalyzer(column)
        self.assertTrue(analisis.has_null_values())
        self.assertEqual(1111, analisis.max_value())
        self.assertEqual(np.int64, type(analisis.max_value()))
        self.assertEqual(1, analisis.min_value())
        self.assertEqual(np.int64, type(analisis.min_value()))
        self.assertEqual(4, analisis.max_length())
        self.assertEqual(np.int64, type(analisis.max_length()))
        self.assertEqual(1, analisis.min_length())
        self.assertEqual(np.int64, type(analisis.min_length()))

    def test_decimal_column(self):
        column_name = "Column decimal"
        column = self.df[column_name]
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertTrue(analisis.has_null_values())
        # Check trailing 0 is not deleted
        self.assertEqual(" 12345.12340", analisis.max_value())
        self.assertEqual("-12345.1", analisis.min_value())
        self.assertEqual(np.int64, type(analisis.max_length_of_integer_part()))
        self.assertEqual(5, analisis.max_length_of_integer_part())
        self.assertEqual([12345.1234, -12345.1], analisis.values_with_max_length_of_integer_part())
        self.assertEqual(np.int64, type(analisis.max_length_of_decimal_part()))
        # Check trailing 0 is not deleted
        self.assertEqual(5, analisis.max_length_of_decimal_part())
        self.assertEqual([12345.1234], analisis.values_with_max_length_of_decimal_part())
        # TODO check values with E (capital e)
        # TODO check values with negative e
        # TODO check with e which are the max and min integer and decimal parts
