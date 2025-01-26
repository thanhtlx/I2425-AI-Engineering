import unittest
import pandas as pd
from data_processing.data_filtering.filter import filter
from data_processing.data_processing import clean
from data_processing.feature_engineering.feature_eng import feature_engineering


class TestFeatureEngineering(unittest.TestCase):

    def setUp(self):
        self.df = clean(filter(pd.read_csv("tests/data.csv")))

    def test_feature_engineering(self):
        # Apply feature engineering
        df_result = feature_engineering(self.df)

        # Test if 'month', 'day', 'year', and 'normalized_amt' columns are created
        self.assertTrue("month" in df_result.columns)
        self.assertTrue("day" in df_result.columns)
        self.assertTrue("year" in df_result.columns)
        self.assertTrue("normalized_amt" in df_result.columns)

        # Check if 'month', 'day', 'year' are correctly extracted from 'trans_date_trans_time'
        self.assertEqual(df_result["month"][1], 7)
        self.assertEqual(df_result["day"][1], 12)
        self.assertEqual(df_result["year"][1], 2020)

        # Test if the normalized amount is computed correctly
        amt_min = df_result["amt"].min()
        amt_max = df_result["amt"].max()
        expected_normalized_amt = (df_result["amt"][0] - amt_min) / (amt_max - amt_min)
        self.assertEqual(df_result["normalized_amt"][0], expected_normalized_amt)

        # Test if the output DataFrame has the correct columns
        expected_columns = [
            "trans_date_trans_time",
            "merchant",
            "category",
            "amt",
            "gender",
            "lat",
            "long",
            "city_pop",
            "job",
            "unix_time",
            "merch_lat",
            "merch_long",
            "label",
            "month",
            "day",
            "year",
            "normalized_amt",
        ]
        self.assertListEqual(list(df_result.columns), expected_columns)

    def test_feature_engineering_with_label(self):
        df_result = feature_engineering(self.df)

        # Check if 'label' column is retained
        self.assertTrue("label" in df_result.columns)

        # Ensure the feature engineering process does not affect the 'label' column
        self.assertEqual(df_result["label"][0], 0)
        self.assertEqual(df_result["label"][4], 1)

    def test_empty_dataframe(self):
        # Test the function with an empty DataFrame
        empty_df = pd.DataFrame(columns=self.df.columns)
        df_result = feature_engineering(empty_df)

        # Ensure the output is still a valid DataFrame but with no rows
        self.assertTrue(df_result.empty)

    def test_invalid_column(self):
        # Test the function with a DataFrame that has an invalid or missing 'trans_date_trans_time' column
        invalid_df = self.df.drop(columns=["trans_date_trans_time"])

        with self.assertRaises(KeyError):
            feature_engineering(invalid_df)


if __name__ == "__main__":
    unittest.main()
