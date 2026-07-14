import unittest
from pathlib import Path


class TestLoader(unittest.TestCase):

    def test_data_folder_exists(self):
        self.assertTrue(Path("data").exists())

    def test_companies_file_exists(self):
        self.assertTrue(Path("data/companies.xlsx").exists())

    def test_profit_file_exists(self):
        self.assertTrue(Path("data/profitandloss.xlsx").exists())

    def test_database_folder_exists(self):
        self.assertTrue(Path("db").exists())


if __name__ == "__main__":
    unittest.main()