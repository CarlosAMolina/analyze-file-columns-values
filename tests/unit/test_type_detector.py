import unittest

import numpy as np
import pandas as pd

from src import type_analyzer as ta


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

    # TODO def test_is_column_of_this_type_is_false_if_e_number_is_decimal(self):
    # TODO     column = pd.Series(data=[" 1.11e1", "2 "], name="values")
    # TODO     self.assertFalse(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())

    # TODO def test_is_column_of_this_type_is_false_if_negative_e(self):
    # TODO     column = pd.Series(data=[" 1e-1", "2 "], name="values")
    # TODO     self.assertFalse(ta._IntegerTypeAnalyzer(column).is_column_of_this_type())


# TODO test decimal if e and E
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

    # TODO def test_is_column_of_this_type_is_false_if_e_number_is_integer(self):
    # TODO     column = pd.Series(data=[" 1e1", "2 "], name="values")
    # TODO     self.assertFalse(ta._DecimalTypeAnalyzer(column).is_column_of_this_type())

    # TODO test negative e, and capital E
