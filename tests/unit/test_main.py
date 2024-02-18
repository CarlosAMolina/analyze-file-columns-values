import pathlib
import unittest

from pandas import DataFrame as Df
import pandas as pd
import numpy as np

from src import main


class TestFileIsReadAsExpected(unittest.TestCase):
    def test_decimal_column(self):
        column_name = "value"
        result = get_df_from_csv_test_file("all_possible_decimal_values.csv")[column_name]
        expected_result = pd.Series(
            data=["3.4", " 12345.12340", " 1.234512340e4", "3", np.nan, "-12345.1"], name=column_name
        )
        pd.testing.assert_series_equal(expected_result, result)


class TestDecimalColumnAnalyzer(unittest.TestCase):
    def test_has_null_values_is_false_if_no_null_values(self):
        column = pd.Series(["1.1"])
        analyzer = main.DecimalColumnAnalyzer(column)
        result = analyzer.has_null_values()
        self.assertFalse(result)

    def test_has_null_values_is_false_if_null_values(self):
        column = pd.Series(["1.1", np.nan])
        analyzer = main.DecimalColumnAnalyzer(column)
        result = analyzer.has_null_values()
        self.assertTrue(result)

    def test_max_value_does_not_remove_trailing_0(self):
        column = pd.Series(data=[" 12345.12340", "3.3"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(" 12345.12340", analisis.max_value())

    def test_max_value_if_null_values(self):
        column = pd.Series(data=["1.1", "2.2", np.nan], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("2.2", analisis.max_value())

    def test_max_value_if_e_number_is_max_value(self):
        column = pd.Series(data=["1.2e3", "3.3"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("1.2e3", analisis.max_value())

    def test_max_value_if_e_number_is_max_value_and_negative(self):
        column = pd.Series(data=["1.2e-1", "0.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("1.2e-1", analisis.max_value())

    def test_max_value_if_e_number_is_not_max_value(self):
        column = pd.Series(data=["1.2e1", "13"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("13", analisis.max_value())

    def test_min_value_if_e_number_is_min_value(self):
        column = pd.Series(data=["-1.2e3", "-1.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("-1.2e3", analisis.min_value())

    def test_min_value_if_null_values(self):
        column = pd.Series(data=["1.1", "2.2", np.nan], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("1.1", analisis.min_value())

    def test_min_value_if_e_number_is_min_value_and_negative(self):
        column = pd.Series(data=["1.2e-1", "0.13"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("1.2e-1", analisis.min_value())

    def test_min_value_if_e_number_is_not_min_value(self):
        column = pd.Series(data=["-1.2e1", "-13.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("-13.1", analisis.min_value())

    def test_max_length_of_integer_part_has_expected_type(self):
        column = pd.Series(data=["-1.2e1", "-13.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analisis.max_length_of_integer_part()))

    def test_max_length_of_integer_part_if_is_the_negative_value(self):
        column = pd.Series(data=["-1234.1", "123.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(4, analisis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_is_the_positive_value(self):
        column = pd.Series(data=["123.1", "-12.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(3, analisis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_e_number_adds_trailing_0(self):
        column = pd.Series(data=["12.3e2", "33.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(4, analisis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_is_e_number_negative(self):
        column = pd.Series(data=["1234.1e-1", "12.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(3, analisis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_is_e_number_negative_drops_integer(self):
        column = pd.Series(data=["1.1e-1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(1, analisis.max_length_of_integer_part())

    def test_df_int_part_is_0_if_e_number_negative_drops_integer(self):
        column = pd.Series(data=["1.1e-1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        analysis_columns_df = analysis._df
        result = analysis_columns_df[f"{analysis._column_name}_int"][0]
        self.assertEqual(0, result)

    def test_values_with_max_length_of_integer_part_if_is_e_number_negative_drops_integer(self):
        column = pd.Series(data=["1.1e-1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["1.1e-1"], analisis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_is_not_afected_by_sign(self):
        column = pd.Series(data=["-1234.123", "1234.123", "11.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["-1234.123", "1234.123"], analisis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_is_not_afected_by_integer_or_decimal_values(self):
        column = pd.Series(data=["12.3", "33.123"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.3", "33.123"], analisis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_if_is_e_number(self):
        column = pd.Series(data=["12.3e2", "33.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.3e2"], analisis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_if_is_e_number_matches_no_e_number(self):
        column = pd.Series(data=["12.3e1", "111.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.3e1", "111.1"], analisis.values_with_max_length_of_integer_part())

    def test_max_length_of_decimal_part_has_expected_type(self):
        column = pd.Series(data=["-1.2e1", "-13.1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analisis.max_length_of_decimal_part()))

    def test_max_length_of_decimal_part_if_no_decimal(self):
        column = pd.Series(data=["12"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        result = analisis.max_length_of_decimal_part()
        self.assertEqual(0, result)

    def test_max_length_of_decimal_part_if_e_number_drops_decimal(self):
        column = pd.Series(data=["-1.2e1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        result = analisis.max_length_of_decimal_part()
        self.assertEqual(0, result)

    def test_max_length_of_decimal_part_does_not_drop_trailing_0(self):
        column = pd.Series(data=["-12.250", "1.11"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(3, analisis.max_length_of_decimal_part())

    def test_df_decimal_value_does_not_drop_trailing_0_with_e_number(self):
        column = pd.Series(data=["1.120e1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        analysis_columns_df = analisis._df
        result = analysis_columns_df[f"{analisis._column_name}_decimal"][0]
        self.assertEqual(20, result)

    def test_max_length_of_decimal_part_does_not_drop_trailing_0_with_e_number(self):
        column = pd.Series(data=["1.120e1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(2, analisis.max_length_of_decimal_part())

    def test_max_length_of_decimal_part_does_not_drop_trailing_0_with_e_number_negative(self):
        column = pd.Series(data=["12.120e-1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(4, analisis.max_length_of_decimal_part())

    def test_values_with_max_length_of_decimal_part_if_e_numbers(self):
        column = pd.Series(data=["12.123e1", "1.11", "1.1", "12.1e-1"], name="values")
        analisis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.123e1", "1.11", "12.1e-1"], analisis.values_with_max_length_of_decimal_part())

    # TODO test methos if there are null values, exmaple, length of columns with null values != 0, must be None


class TestAnalyzerClassesReadFromFile(unittest.TestCase):
    def setUp(self):
        self.df = get_df_from_csv_test_file("file.csv")

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
        self.assertEqual(
            [" 12345.12340", " 1.234512340e4", "-12345.1"], analisis.values_with_max_length_of_integer_part()
        )
        self.assertEqual(np.int64, type(analisis.max_length_of_decimal_part()))
        # Check trailing 0 is not deleted
        self.assertEqual(5, analisis.max_length_of_decimal_part())
        self.assertEqual([" 12345.12340", " 1.234512340e4"], analisis.values_with_max_length_of_decimal_part())
        # TODO check values with E (capital e)
        # TODO check values with negative e
        # TODO check with e which are the max and min integer and decimal parts


def get_df_from_csv_test_file(file_name: str) -> Df:
    script_dir = pathlib.Path(__file__).parent.absolute()
    tests_dir = script_dir.parent
    csv_file_path_name = str(pathlib.PurePath(tests_dir, "files", file_name))
    return main.get_df_from_csv(csv_file_path_name)
