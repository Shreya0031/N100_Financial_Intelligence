import unittest
from pathlib import Path
import pandas as pd


class TestValidator(unittest.TestCase):

    def test_validation_report_exists(self):
        self.assertTrue(Path("output/validation_failures.csv").exists())

    def test_validation_report_not_empty(self):
        df = pd.read_csv("output/validation_failures.csv")
        self.assertGreater(len(df), 0)

    def test_load_audit_exists(self):
        self.assertTrue(Path("output/load_audit.csv").exists())

    def test_load_audit_not_empty(self):
        df = pd.read_csv("output/load_audit.csv")
        self.assertGreater(len(df), 0)


if __name__ == "__main__":
    unittest.main()