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


class TestStringColumnAnalyzer(unittest.TestCase):
    def test_has_null_values_is_false_if_no_null_values(self):
        column = pd.Series(["a", "b"])
        analysis = main.StringColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertFalse(result)

    def test_has_null_values_is_false_if_null_values(self):
        column = pd.Series(["a", np.nan])
        analysis = main.StringColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertTrue(result)

    def test_has_empty_values_if_stripped_is_false(self):
        column = pd.Series(data=[" a"], name="values")
        analysis = main.StringColumnAnalyzer(column)
        result = analysis.has_empty_values_if_stripped()
        self.assertFalse(result)

    def test_has_empty_values_if_stripped_is_true(self):
        column = pd.Series(data=[" "], name="values")
        analysis = main.StringColumnAnalyzer(column)
        result = analysis.has_empty_values_if_stripped()
        self.assertTrue(result)

    def test_has_empty_values_if_no_stripped_is_false(self):
        column = pd.Series(data=[" "], name="values")
        analysis = main.StringColumnAnalyzer(column)
        result = analysis.has_empty_values_if_no_stripped()
        self.assertFalse(result)

    def test_has_empty_values_if_no_stripped_is_true(self):
        column = pd.Series(data=[""], name="values")
        analysis = main.StringColumnAnalyzer(column)
        result = analysis.has_empty_values_if_no_stripped()
        self.assertTrue(result)


class TestIntegerColumnAnalyzer(unittest.TestCase):
    def test_has_null_values_is_false_if_no_null_values(self):
        column = pd.Series(["1"])
        analysis = main.IntegerColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertFalse(result)

    def test_has_null_values_is_false_if_null_values(self):
        column = pd.Series(["1", np.nan])
        analysis = main.IntegerColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertTrue(result)

    def test_max_value(self):
        column = pd.Series(data=["-1", "2", np.nan], name="values")
        analysis = main.IntegerColumnAnalyzer(column)
        result = analysis.max_value()
        self.assertEqual(2, result)

    def test_min_value(self):
        column = pd.Series(data=["-1", "2", np.nan], name="values")
        analysis = main.IntegerColumnAnalyzer(column)
        result = analysis.min_value()
        self.assertEqual(-1, result)

    def test_max_length_has_expected_type(self):
        column = pd.Series(data=["-123", "2", np.nan], name="values")
        analysis = main.IntegerColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analysis.max_length()))

    def test_max_length_is_not_affected_by_negative_numbers(self):
        column = pd.Series(data=["-123", "2", np.nan], name="values")
        analysis = main.IntegerColumnAnalyzer(column)
        result = analysis.max_length()
        self.assertEqual(3, result)

    def test_min_length_has_expected_type(self):
        column = pd.Series(data=["-123", "2", np.nan], name="values")
        analysis = main.IntegerColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analysis.min_length()))

    def test_min_length_is_not_affected_by_negative_numbers(self):
        column = pd.Series(data=["-2", "12", np.nan], name="values")
        analysis = main.IntegerColumnAnalyzer(column)
        result = analysis.min_length()
        self.assertEqual(1, result)


class TestDecimalColumnAnalyzer(unittest.TestCase):
    def test_has_null_values_is_false_if_no_null_values(self):
        column = pd.Series(["1.1"])
        analysis = main.DecimalColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertFalse(result)

    def test_has_null_values_is_false_if_null_values(self):
        column = pd.Series(["1.1", np.nan])
        analysis = main.DecimalColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertTrue(result)

    def test_max_value_does_not_remove_trailing_0(self):
        column = pd.Series(data=[" 12345.12340", "3.3"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(" 12345.12340", analysis.max_value())

    def test_max_value_if_null_values(self):
        column = pd.Series(data=["1.1", "2.2", np.nan], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("2.2", analysis.max_value())

    def test_max_value_if_e_number_is_max_value(self):
        column = pd.Series(data=["1.2e3", "3.3"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("1.2e3", analysis.max_value())

    def test_max_value_if_e_number_is_max_value_and_negative(self):
        column = pd.Series(data=["1.2e-1", "0.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("1.2e-1", analysis.max_value())

    def test_max_value_if_e_number_is_not_max_value(self):
        column = pd.Series(data=["1.2e1", "13"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("13", analysis.max_value())

    def test_min_value_if_e_number_is_min_value(self):
        column = pd.Series(data=["-1.2e3", "-1.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("-1.2e3", analysis.min_value())

    def test_min_value_if_null_values(self):
        column = pd.Series(data=["1.1", "2.2", np.nan], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("1.1", analysis.min_value())

    def test_min_value_if_e_number_is_min_value_and_negative(self):
        column = pd.Series(data=["1.2e-1", "0.13"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("1.2e-1", analysis.min_value())

    def test_min_value_if_e_number_is_not_min_value(self):
        column = pd.Series(data=["-1.2e1", "-13.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual("-13.1", analysis.min_value())

    def test_max_length_of_integer_part_has_expected_type(self):
        column = pd.Series(data=["-1.2e1", "-13.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analysis.max_length_of_integer_part()))

    def test_max_length_of_integer_part_if_is_the_negative_value(self):
        column = pd.Series(data=["-1234.1", "123.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(4, analysis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_is_the_positive_value(self):
        column = pd.Series(data=["123.1", "-12.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(3, analysis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_e_number_adds_trailing_0(self):
        column = pd.Series(data=["12.3e2", "33.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(4, analysis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_is_e_number_negative(self):
        column = pd.Series(data=["1234.1e-1", "12.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(3, analysis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_is_e_number_negative_drops_integer(self):
        column = pd.Series(data=["1.1e-1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(1, analysis.max_length_of_integer_part())

    def test_df_int_part_is_0_if_e_number_negative_drops_integer(self):
        column = pd.Series(data=["1.1e-1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        analysis_columns_df = analysis._df
        result = analysis_columns_df[f"{analysis._column_name}_int"][0]
        self.assertEqual(0, result)

    def test_values_with_max_length_of_integer_part_if_is_e_number_negative_drops_integer(self):
        column = pd.Series(data=["1.1e-1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["1.1e-1"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_is_not_afected_by_sign(self):
        column = pd.Series(data=["-1234.123", "1234.123", "11.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["-1234.123", "1234.123"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_is_not_afected_by_integer_or_decimal_values(self):
        column = pd.Series(data=["12.3", "33.123"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.3", "33.123"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_if_is_e_number(self):
        column = pd.Series(data=["12.3e2", "33.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.3e2"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_if_is_e_number_matches_no_e_number(self):
        column = pd.Series(data=["12.3e1", "111.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.3e1", "111.1"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_returns_original_value_without_modifications(self):
        column = pd.Series(data=[" 12.1", "1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual([" 12.1"], analysis.values_with_max_length_of_decimal_part())

    def test_max_length_of_decimal_part_has_expected_type(self):
        column = pd.Series(data=["-1.2e1", "-13.1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analysis.max_length_of_decimal_part()))

    def test_max_length_of_decimal_part_if_no_decimal(self):
        column = pd.Series(data=["12"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        result = analysis.max_length_of_decimal_part()
        self.assertEqual(0, result)

    def test_max_length_of_decimal_part_if_e_number_drops_decimal(self):
        column = pd.Series(data=["-1.2e1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        result = analysis.max_length_of_decimal_part()
        self.assertEqual(0, result)

    def test_max_length_of_decimal_part_does_not_drop_trailing_0(self):
        column = pd.Series(data=["-12.250", "1.11"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(3, analysis.max_length_of_decimal_part())

    def test_df_decimal_value_does_not_drop_trailing_0_with_e_number(self):
        column = pd.Series(data=["1.120e1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        analysis_columns_df = analysis._df
        result = analysis_columns_df[f"{analysis._column_name}_decimal"][0]
        self.assertEqual(20, result)

    def test_df_decimal_value_is_none_for_no_decimal_values(self):
        column = pd.Series(data=["1.2", "1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        analysis_columns_df = analysis._df
        column_name = f"{analysis._column_name}_decimal"
        result = analysis_columns_df[column_name]
        expected_result = pd.Series(data=[2, np.nan], name=column_name).astype("Int64")
        pd.testing.assert_series_equal(expected_result, result)

    def test_max_length_of_decimal_part_does_not_drop_trailing_0_with_e_number(self):
        column = pd.Series(data=["1.120e1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(2, analysis.max_length_of_decimal_part())

    def test_max_length_of_decimal_part_does_not_drop_trailing_0_with_e_number_negative(self):
        column = pd.Series(data=["12.120e-1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(4, analysis.max_length_of_decimal_part())

    def test_values_with_max_length_of_decimal_part_if_e_numbers(self):
        column = pd.Series(data=["12.123e1", "1.11", "1.1", "12.1e-1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.123e1", "1.11", "12.1e-1"], analysis.values_with_max_length_of_decimal_part())

    def test_values_with_max_length_of_decimal_part_returns_original_value_without_modifications(self):
        column = pd.Series(data=[" 1.12", "1"], name="values")
        analysis = main.DecimalColumnAnalyzer(column)
        self.assertEqual([" 1.12"], analysis.values_with_max_length_of_decimal_part())


class TestAnalyzerClassesReadFromFile(unittest.TestCase):
    def setUp(self):
        self.df = get_df_from_csv_test_file("file.csv")

    def test_string_column_if_null_values(self):
        column_name = "Column string"
        column = self.df[column_name]
        analysis = main.StringColumnAnalyzer(column)
        self.assertTrue(analysis.has_null_values())
        self.assertFalse(analysis.has_empty_values_if_no_stripped())
        self.assertTrue(analysis.has_empty_values_if_stripped())
        self.assertEqual(7, analysis.max_length_if_stripped())
        self.assertEqual(9, analysis.max_length_if_no_stripped())
        self.assertEqual(0, analysis.min_length_if_stripped())
        self.assertEqual(1, analysis.min_length_if_no_stripped())
        self.assertEqual(1, analysis.min_length_if_no_stripped())
        self.assertEqual(["Foo Bar", "Bar Foo"], analysis.max_values_if_stripped())
        self.assertEqual([" Foo Bar "], analysis.max_values_if_no_stripped())
        self.assertEqual([""], analysis.min_values_if_stripped())
        self.assertEqual([" "], analysis.min_values_if_no_stripped())

    def test_string_column_if_no_null_values(self):
        column_name = "Column string all lines with value"
        column = self.df[column_name]
        analysis = main.StringColumnAnalyzer(column)
        self.assertFalse(analysis.has_null_values())

    def test_integer_column(self):
        column_name = "Column integer"
        column = self.df[column_name]
        analysis = main.IntegerColumnAnalyzer(column)
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
        analysis = main.DecimalColumnAnalyzer(column)
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
        # TODO check values with E (capital e)
        # TODO check values with negative e
        # TODO check with e which are the max and min integer and decimal parts


def get_df_from_csv_test_file(file_name: str) -> Df:
    script_dir = pathlib.Path(__file__).parent.absolute()
    tests_dir = script_dir.parent
    csv_file_path_name = str(pathlib.PurePath(tests_dir, "files", file_name))
    return main.get_df_from_csv(csv_file_path_name)
