import unittest

import numpy as np
import pandas as pd

from src import type_analyzer as ta


class TestFunction_get_column_type(unittest.TestCase):
    # Note. Columns are read as strings.
    def test_if_column_is_integer(self):
        column = pd.Series(data=["1", "2", np.nan], name="values")
        self.assertEqual(ta.Type.INTEGER, ta.get_column_type(column))

    def test_if_column_is_decimal(self):
        column = pd.Series(data=["1.0", "2"], name="values")
        self.assertEqual(ta.Type.DECIMAL, ta.get_column_type(column))

    def test_if_column_is_string(self):
        column = pd.Series(data=["a", "2"], name="values")
        self.assertEqual(ta.Type.STRING, ta.get_column_type(column))


class TestIntegerTypeAnalyzer(unittest.TestCase):
    # Note. Columns are read as strings.
    def test_is_column_of_this_type_is_true_if_integers(self):
        column = pd.Series(data=["1", "2"], name="values")
        self.assertTrue(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_integers_and_null(self):
        column = pd.Series(data=["1", np.nan], name="values")
        self.assertTrue(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_false_if_has_strings(self):
        column = pd.Series(data=["a", "2"], name="values")
        self.assertFalse(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_false_if_has_float(self):
        column = pd.Series(data=["1.0", "2"], name="values")
        self.assertFalse(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_white_space(self):
        column = pd.Series(data=[" ", "2"], name="values")
        self.assertTrue(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_trail_and_lead_white_space(self):
        column = pd.Series(data=[" 1", "2 "], name="values")
        self.assertTrue(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_e_number_is_not_decimal(self):
        column = pd.Series(data=[" 1e1", "2 "], name="values")
        self.assertTrue(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_false_if_e_number_is_decimal_with_leading_decimal_ceros(self):
        column = pd.Series(data=[" 1.001e1", "2 "], name="values")
        self.assertFalse(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_false_if_negative_e(self):
        column = pd.Series(data=[" 1e-1", "2 "], name="values")
        self.assertFalse(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())


class TestDecimalTypeAnalyzer(unittest.TestCase):
    # Note. Columns are read as strings.
    def test_is_column_of_this_type_is_false_if_integers(self):
        column = pd.Series(data=["1", "2"], name="values")
        self.assertFalse(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_floats(self):
        column = pd.Series(data=["1.1", "2.2"], name="values")
        self.assertTrue(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_float_and_null(self):
        column = pd.Series(data=["1.0", np.nan], name="values")
        self.assertTrue(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_false_if_has_strings(self):
        column = pd.Series(data=["a", "2.1"], name="values")
        self.assertFalse(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_has_float_and_integer(self):
        column = pd.Series(data=["1.0", "2"], name="values")
        self.assertTrue(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_white_space(self):
        column = pd.Series(data=[" ", "2.0"], name="values")
        self.assertTrue(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_trail_and_lead_white_space(self):
        column = pd.Series(data=[" 1.1", "2 "], name="values")
        self.assertTrue(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_e_number(self):
        column = pd.Series(data=["1.12e1", "2"], name="values")
        self.assertTrue(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_captital_e_number(self):
        column = pd.Series(data=["1.12E1", "2"], name="values")
        self.assertTrue(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_false_if_e_number_is_integer(self):
        column = pd.Series(data=["1e1", "2"], name="values")
        self.assertFalse(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_e_number_is_decimal_with_leading_decimal_ceros(self):
        column = pd.Series(data=["1.001e1", "2"], name="values")
        self.assertTrue(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_true_if_negative_e(self):
        column = pd.Series(data=["1e-1", "2"], name="values")
        self.assertTrue(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

# TODO test _are_all_characters_e with null value because it raises exception
