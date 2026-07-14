import unittest
from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,    
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover,
)

class TestRatios(unittest.TestCase):

    def test_net_profit_margin(self):
        self.assertEqual(net_profit_margin(200, 1000), 20.0)

    def test_net_profit_margin_zero_sales(self):
        self.assertIsNone(net_profit_margin(200, 0))

    def test_operating_profit_margin(self):
        self.assertEqual(operating_profit_margin(300, 1000), 30.0)

    def test_return_on_equity(self):
        self.assertEqual(return_on_equity(200, 500, 500), 20.0)

    def test_return_on_equity_negative(self):
        self.assertIsNone(return_on_equity(200, -500, 200))

    def test_return_on_capital_employed(self):
        self.assertEqual(return_on_capital_employed(300, 500, 500, 200), 25.0)

    def test_return_on_assets(self):
        self.assertEqual(return_on_assets(200, 2500), 8.0)

    def test_return_on_assets_zero(self):
        self.assertIsNone(return_on_assets(200, 0))


    def test_return_on_assets_zero(self):
        self.assertIsNone(return_on_assets(200, 0))

    # ---------------------------
    # Day 09 Tests
    # ---------------------------

    def test_debt_to_equity(self):
        self.assertEqual(debt_to_equity(200, 500, 500), 0.2)

    def test_debt_free(self):
        self.assertEqual(debt_to_equity(0, 500, 500), 0)

    def test_high_leverage(self):
        self.assertTrue(high_leverage_flag(6, "Technology"))

    def test_financial_sector(self):
        self.assertFalse(high_leverage_flag(8, "Financials"))
        
    def test_interest_coverage(self):
        self.assertEqual(
            interest_coverage_ratio(300, 100, 100),
            4.0
        )

    def test_interest_zero(self):
        self.assertIsNone(
            interest_coverage_ratio(300, 100, 0)
        )

    def test_icr_label(self):
        self.assertEqual(icr_label(0), "Debt Free")

    def test_asset_turnover(self):
        self.assertEqual(asset_turnover(1000, 500), 2.0)

if __name__ == "__main__":
    unittest.main()