import unittest

import pandas as pd

from src import type_detector as td


class TestIntegerTypeDetector(unittest.TestCase):
    # Note. Columns are ridden as strings.
    # TODO test integer if null values (pandas convert ints to floats)
    def test_is_column_of_this_type_is_true_if_integers(self):
        column = pd.Series(data=["1", "2"], name="values")
        self.assertTrue(td.IntegerTypeDetector(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_false_if_has_strings(self):
        column = pd.Series(data=["a", "2"], name="values")
        self.assertFalse(td.IntegerTypeDetector(column).is_column_of_this_type())

    def test_is_column_of_this_type_is_false_if_has_float(self):
        column = pd.Series(data=["1.0", "2"], name="values")
        self.assertFalse(td.IntegerTypeDetector(column).is_column_of_this_type())


# TODO test decimal if e and E
