import unittest
import pandas as pd
from data_processing.data_filtering.filter import filter

class TestDataFilter(unittest.TestCase):
    def setUp(self):
        self.df = pd.read_csv("tests/data.csv")

    def test_filter(self):
        df_filtered = filter(self.df)
        
        # Assert there are no duplicate rows
        self.assertEqual(df_filtered.duplicated().sum(), 0)
        
        # Assert no NaN values
        self.assertFalse(df_filtered.isnull().values.any())
        
        # Assert the amount column has only positive values
        self.assertTrue((df_filtered["amt"] > 0).all())

if __name__ == "__main__":
    unittest.main()
