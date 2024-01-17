import pathlib
import unittest

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

    def test_string_column_if_no_null_values(self):
        column_name = "Column string all lines with value"
        column = self.df[column_name]
        analisis = main.StringColumnAnalyzer(column)
        self.assertFalse(analisis.has_null_values())
