import unittest
from src.etl.normaliser import normalize_year, normalize_ticker


class TestNormaliser(unittest.TestCase):

    def test_normalize_year_integer(self):
        self.assertEqual(normalize_year(2024), 2024)

    def test_normalize_year_string(self):
        self.assertEqual(normalize_year("2023"), 2023)

    def test_normalize_ticker_uppercase(self):
        self.assertEqual(normalize_ticker("abb"), "ABB")

    def test_normalize_ticker_strip_spaces(self):
        self.assertEqual(normalize_ticker("  tcs "), "TCS")


if __name__ == "__main__":
    unittest.main()