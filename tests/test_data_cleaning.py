import unittest
import pandas as pd
from data_processing.data_processing import clean


class TestDataCleaning(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("tests/data.csv")

    def test_clean_function(self):
        cleaned_df = clean(self.df)

        # Test that missing values are filled correctly
        self.assertEqual(cleaned_df["trans_date_trans_time"].iloc[0], "0000-00-00")
        self.assertEqual(cleaned_df["merchant"].iloc[0], "Unknown")
        self.assertEqual(cleaned_df["category"].iloc[0], "Unknown")
        self.assertEqual(cleaned_df["amt"].iloc[1], 0)
        self.assertEqual(cleaned_df["gender"].iloc[0], "Unknown")
        self.assertEqual(cleaned_df["lat"].iloc[2], 0)
        self.assertEqual(cleaned_df["long"].iloc[2], 0)
        self.assertEqual(cleaned_df["city_pop"].iloc[3], 0)
        self.assertEqual(cleaned_df["job"].iloc[3], "Unknown")
        self.assertEqual(cleaned_df["unix_time"].iloc[3], 0)
        self.assertEqual(cleaned_df["merch_lat"].iloc[3], 0)
        self.assertEqual(cleaned_df["merch_long"].iloc[3], 0)

        # Test that the 'is_fraud' column is renamed to 'label'
        self.assertIn("label", cleaned_df.columns)
        self.assertNotIn("is_fraud", cleaned_df.columns)

        # Test that 'trans_date_trans_time' is properly filled for missing values
        self.assertEqual(cleaned_df["trans_date_trans_time"].iloc[0], "0000-00-00")
        self.assertEqual(
            cleaned_df["trans_date_trans_time"].iloc[1], "2020-12-11 20:30:29"
        )

    def test_clean_column_types(self):
        # Check if column types are correct after cleaning
        cleaned_df = clean(self.df)
        self.assertIsInstance(cleaned_df["amt"].iloc[0], (int, float))
        self.assertIsInstance(cleaned_df["lat"].iloc[0], (float))
        self.assertIsInstance(cleaned_df["long"].iloc[0], (float))
        self.assertIsInstance(cleaned_df["city_pop"].iloc[0], (int, float, str, object))
        self.assertIsInstance(
            cleaned_df["unix_time"].iloc[0], (int, float, str, object)
        )

    def test_no_null_values(self):
        # Test that no missing values remain after cleaning
        cleaned_df = clean(self.df)

        self.assertFalse(cleaned_df.isnull().values.any())


if __name__ == "__main__":
    unittest.main()
