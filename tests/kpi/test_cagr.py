import unittest
from src.analytics.cagr import calculate_cagr


class TestCAGR(unittest.TestCase):

    def test_normal_cagr(self):
        value, flag = calculate_cagr(100, 200, 5)
        self.assertIsNotNone(value)
        self.assertIsNone(flag)

    def test_decline_to_loss(self):
        value, flag = calculate_cagr(100, -50, 5)
        self.assertIsNone(value)
        self.assertEqual(flag, "DECLINE_TO_LOSS")

    def test_turnaround(self):
        value, flag = calculate_cagr(-100, 50, 5)
        self.assertIsNone(value)
        self.assertEqual(flag, "TURNAROUND")

    def test_both_negative(self):
        value, flag = calculate_cagr(-100, -50, 5)
        self.assertIsNone(value)
        self.assertEqual(flag, "BOTH_NEGATIVE")

    def test_zero_base(self):
        value, flag = calculate_cagr(0, 100, 5)
        self.assertIsNone(value)
        self.assertEqual(flag, "ZERO_BASE")

    def test_invalid_period(self):
        value, flag = calculate_cagr(100, 200, 0)
        self.assertIsNone(value)
        self.assertEqual(flag, "INVALID_PERIOD")

    def test_positive_growth(self):
        value, flag = calculate_cagr(100, 300, 10)
        self.assertGreater(value, 0)
        self.assertIsNone(flag)

    def test_negative_growth(self):
        value, flag = calculate_cagr(300, 100, 5)
        self.assertLess(value, 0)
        self.assertIsNone(flag)

    def test_same_values(self):
        value, flag = calculate_cagr(100, 100, 5)
        self.assertEqual(value, 0.0)
        self.assertIsNone(flag)

    def test_small_growth(self):
        value, flag = calculate_cagr(100, 110, 5)
        self.assertGreater(value, 0)
        self.assertIsNone(flag)


if __name__ == "__main__":
    unittest.main()