import unittest

import pandas as pd
import numpy as np

from src import value_analyzer


class TestShowAnalysis(unittest.TestCase):
    def test_show_decimal_column_analysis(self):
        column = pd.Series(
            data=["3.4", " 12345.12340", " 1.2345123410e4", "3", np.nan, "-12345.1"], name="random decimal numbers"
        )
        value_analyzer.show_decimal_column_analysis(column)

    def test_show_integer_column_analysis(self):
        column = pd.Series(data=["1234", " 2", np.nan, "-3"], name="random integer numbers")
        value_analyzer.show_integer_column_analysis(column)

    def test_show_string_column_analysis(self):
        column = pd.Series(data=[" john doe", "johnny ", np.nan, "doe", " "], name="names")
        value_analyzer.show_string_column_analysis(column)


class TestStringColumnAnalyzer(unittest.TestCase):
    def test_has_null_values_is_false_if_no_null_values(self):
        column = pd.Series(["a", "b"])
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertFalse(result)

    def test_has_null_values_is_false_if_null_values(self):
        column = pd.Series(["a", np.nan])
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertTrue(result)

    def test_has_empty_values_if_stripped_is_false(self):
        column = pd.Series(data=[" a"], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.has_empty_values_if_stripped()
        self.assertFalse(result)

    def test_has_empty_values_if_stripped_is_true(self):
        column = pd.Series(data=[" "], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.has_empty_values_if_stripped()
        self.assertTrue(result)

    def test_has_empty_values_if_no_stripped_is_false(self):
        column = pd.Series(data=[" "], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.has_empty_values_if_no_stripped()
        self.assertFalse(result)

    def test_has_empty_values_if_no_stripped_is_true(self):
        column = pd.Series(data=[""], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.has_empty_values_if_no_stripped()
        self.assertTrue(result)

    def test_max_length_if_stripped(self):
        column = pd.Series(data=["a ", "b"], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.max_length_if_stripped()
        self.assertEqual(1, result)

    def test_max_length_if_no_stripped(self):
        column = pd.Series(data=["a ", "b"], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.max_length_if_no_stripped()
        self.assertEqual(2, result)

    def test_min_length_if_stripped(self):
        column = pd.Series(data=["a ", "bb"], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.min_length_if_stripped()
        self.assertEqual(1, result)

    def test_min_length_if_no_stripped(self):
        column = pd.Series(data=["a ", "abc"], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.min_length_if_no_stripped()
        self.assertEqual(2, result)

    def test_max_values_if_stripped(self):
        column = pd.Series(data=["ab ", "cd", np.nan], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.max_values_if_stripped()
        self.assertEqual(["ab", "cd"], result)

    def test_max_values_if_no_stripped(self):
        column = pd.Series(data=["ab ", "cd", "abc", np.nan], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.max_values_if_no_stripped()
        self.assertEqual(["ab ", "abc"], result)

    def test_min_values_if_stripped(self):
        column = pd.Series(data=["a ", "b", "cd", np.nan], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.min_values_if_stripped()
        self.assertEqual(["a", "b"], result)

    def test_min_values_if_no_stripped(self):
        column = pd.Series(data=["a ", "b", "cd", np.nan], name="values")
        analysis = value_analyzer.StringColumnAnalyzer(column)
        result = analysis.min_values_if_no_stripped()
        self.assertEqual(["b"], result)


class TestIntegerColumnAnalyzer(unittest.TestCase):
    def test_has_null_values_is_false_if_no_null_values(self):
        column = pd.Series(["1"])
        analysis = value_analyzer.IntegerColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertFalse(result)

    def test_has_null_values_is_false_if_null_values(self):
        column = pd.Series(["1", np.nan])
        analysis = value_analyzer.IntegerColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertTrue(result)

    def test_max_value(self):
        column = pd.Series(data=["-1", "2", np.nan], name="values")
        analysis = value_analyzer.IntegerColumnAnalyzer(column)
        result = analysis.max_value()
        self.assertEqual(2, result)

    def test_min_value(self):
        column = pd.Series(data=["-1", "2", np.nan], name="values")
        analysis = value_analyzer.IntegerColumnAnalyzer(column)
        result = analysis.min_value()
        self.assertEqual(-1, result)

    def test_max_length_has_expected_type(self):
        column = pd.Series(data=["-123", "2", np.nan], name="values")
        analysis = value_analyzer.IntegerColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analysis.max_length()))

    def test_max_length_is_not_affected_by_negative_numbers(self):
        column = pd.Series(data=["-123", "2", np.nan], name="values")
        analysis = value_analyzer.IntegerColumnAnalyzer(column)
        result = analysis.max_length()
        self.assertEqual(3, result)

    def test_min_length_has_expected_type(self):
        column = pd.Series(data=["-123", "2", np.nan], name="values")
        analysis = value_analyzer.IntegerColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analysis.min_length()))

    def test_min_length_is_not_affected_by_negative_numbers(self):
        column = pd.Series(data=["-2", "12", np.nan], name="values")
        analysis = value_analyzer.IntegerColumnAnalyzer(column)
        result = analysis.min_length()
        self.assertEqual(1, result)


class TestDecimalColumnAnalyzer(unittest.TestCase):
    def test_has_null_values_is_false_if_no_null_values(self):
        column = pd.Series(["1.1"])
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertFalse(result)

    def test_has_null_values_is_false_if_null_values(self):
        column = pd.Series(["1.1", np.nan])
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        result = analysis.has_null_values()
        self.assertTrue(result)

    def test_max_value_does_not_remove_trailing_0(self):
        column = pd.Series(data=[" 12345.12340", "3.3"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(" 12345.12340", analysis.max_value())

    def test_max_value_if_null_values(self):
        column = pd.Series(data=["1.1", "2.2", np.nan], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual("2.2", analysis.max_value())

    def test_max_value_if_e_number_is_max_value(self):
        column = pd.Series(data=["1.2e3", "3.3"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual("1.2e3", analysis.max_value())

    def test_max_value_if_e_number_is_max_value_and_negative(self):
        column = pd.Series(data=["1.2e-1", "0.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual("1.2e-1", analysis.max_value())

    def test_max_value_if_e_number_is_not_max_value(self):
        column = pd.Series(data=["1.2e1", "13"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual("13", analysis.max_value())

    def test_min_value_if_e_number_is_min_value(self):
        column = pd.Series(data=["-1.2e3", "-1.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual("-1.2e3", analysis.min_value())

    def test_min_value_if_null_values(self):
        column = pd.Series(data=["1.1", "2.2", np.nan], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual("1.1", analysis.min_value())

    def test_min_value_if_e_number_is_min_value_and_negative(self):
        column = pd.Series(data=["1.2e-1", "0.13"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual("1.2e-1", analysis.min_value())

    def test_min_value_if_e_number_is_not_min_value(self):
        column = pd.Series(data=["-1.2e1", "-13.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual("-13.1", analysis.min_value())

    def test_max_length_of_integer_part_has_expected_type(self):
        column = pd.Series(data=["-1.2e1", "-13.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analysis.max_length_of_integer_part()))

    def test_max_length_of_integer_part_if_is_the_negative_value(self):
        column = pd.Series(data=["-1234.1", "123.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(4, analysis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_is_the_positive_value(self):
        column = pd.Series(data=["123.1", "-12.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(3, analysis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_e_number_adds_trailing_0(self):
        column = pd.Series(data=["12.3e2", "33.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(4, analysis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_is_e_number_negative(self):
        column = pd.Series(data=["1234.1e-1", "12.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(3, analysis.max_length_of_integer_part())

    def test_max_length_of_integer_part_if_is_e_number_negative_drops_integer(self):
        column = pd.Series(data=["1.1e-1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(1, analysis.max_length_of_integer_part())

    def test_df_int_part_is_0_if_e_number_negative_drops_integer(self):
        column = pd.Series(data=["1.1e-1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        analysis_columns_df = analysis._df
        result = analysis_columns_df[f"{analysis._column_name}_int"][0]
        self.assertEqual(0, result)

    def test_values_with_max_length_of_integer_part_if_is_e_number_negative_drops_integer(self):
        column = pd.Series(data=["1.1e-1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(["1.1e-1"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_is_not_afected_by_sign(self):
        column = pd.Series(data=["-1234.123", "1234.123", "11.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(["-1234.123", "1234.123"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_is_not_afected_by_integer_or_decimal_values(self):
        column = pd.Series(data=["12.3", "33.123"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.3", "33.123"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_if_is_e_number(self):
        column = pd.Series(data=["12.3e2", "33.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.3e2"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_if_is_e_number_matches_no_e_number(self):
        column = pd.Series(data=["12.3e1", "111.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.3e1", "111.1"], analysis.values_with_max_length_of_integer_part())

    def test_values_with_max_length_of_integer_part_returns_original_value_without_modifications(self):
        column = pd.Series(data=[" 12.1", "1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual([" 12.1"], analysis.values_with_max_length_of_decimal_part())

    def test_max_length_of_decimal_part_has_expected_type(self):
        column = pd.Series(data=["-1.2e1", "-13.1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(np.int64, type(analysis.max_length_of_decimal_part()))

    def test_max_length_of_decimal_part_if_no_decimal(self):
        column = pd.Series(data=["12"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        result = analysis.max_length_of_decimal_part()
        self.assertEqual(0, result)

    def test_max_length_of_decimal_part_if_e_number_drops_decimal(self):
        column = pd.Series(data=["-1.2e1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        result = analysis.max_length_of_decimal_part()
        self.assertEqual(0, result)

    def test_max_length_of_decimal_part_does_not_drop_trailing_0(self):
        column = pd.Series(data=["-12.250", "1.11"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(3, analysis.max_length_of_decimal_part())

    def test_df_decimal_value_does_not_drop_trailing_0_with_e_number(self):
        column = pd.Series(data=["1.120e1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        analysis_columns_df = analysis._df
        result = analysis_columns_df[f"{analysis._column_name}_decimal"][0]
        self.assertEqual(20, result)

    def test_df_decimal_value_is_none_for_no_decimal_values(self):
        column = pd.Series(data=["1.2", "1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        analysis_columns_df = analysis._df
        column_name = f"{analysis._column_name}_decimal"
        result = analysis_columns_df[column_name]
        expected_result = pd.Series(data=[2, np.nan], name=column_name).astype("Int64")
        pd.testing.assert_series_equal(expected_result, result)

    def test_max_length_of_decimal_part_does_not_drop_trailing_0_with_e_number(self):
        column = pd.Series(data=["1.120e1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(2, analysis.max_length_of_decimal_part())

    def test_max_length_of_decimal_part_does_not_drop_trailing_0_with_e_number_negative(self):
        column = pd.Series(data=["12.120e-1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(4, analysis.max_length_of_decimal_part())

    def test_values_with_max_length_of_decimal_part_if_e_numbers(self):
        column = pd.Series(data=["12.123e1", "1.11", "1.1", "12.1e-1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual(["12.123e1", "1.11", "12.1e-1"], analysis.values_with_max_length_of_decimal_part())

    def test_values_with_max_length_of_decimal_part_returns_original_value_without_modifications(self):
        column = pd.Series(data=[" 1.12", "1"], name="values")
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        self.assertEqual([" 1.12"], analysis.values_with_max_length_of_decimal_part())

    def test_get_df_add_analysis_columns_works_with_capital_e(self):
        column_name = "values"
        column = pd.Series(data=["1.12e1", "1.123E2"], name=column_name)
        analysis = value_analyzer.DecimalColumnAnalyzer(column)
        df = analysis._get_df_add_analysis_columns()
        expected_result = pd.Series(data=["11.2", "112.3"], name=f"{column_name}_numeric_str")
        pd.testing.assert_series_equal(expected_result, df[f"{column_name}_numeric_str"])
