import unittest

from src.analytics.cashflow_kpis import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


class TestCashflowKPIs(unittest.TestCase):

    # -----------------------------
    # Free Cash Flow
    # -----------------------------

    def test_free_cash_flow(self):
        self.assertEqual(
            free_cash_flow(500, -200),
            300
        )

    def test_free_cash_flow_negative(self):
        self.assertEqual(
            free_cash_flow(-100, -200),
            -300
        )

    # -----------------------------
    # CFO Quality
    # -----------------------------

    def test_cfo_quality_high(self):
        self.assertEqual(
            cfo_quality_score(300, 200),
            "High Quality"
        )

    def test_cfo_quality_moderate(self):
        self.assertEqual(
            cfo_quality_score(120, 200),
            "Moderate"
        )

    def test_cfo_quality_low(self):
        self.assertEqual(
            cfo_quality_score(50, 200),
            "Accrual Risk"
        )

    def test_cfo_quality_zero_pat(self):
        self.assertIsNone(
            cfo_quality_score(100, 0)
        )

    # -----------------------------
    # CapEx Intensity
    # -----------------------------

    def test_capex_asset_light(self):
        self.assertEqual(
            capex_intensity(-20, 1000),
            "Asset Light"
        )

    def test_capex_moderate(self):
        self.assertEqual(
            capex_intensity(-50, 1000),
            "Moderate"
        )

    def test_capex_capital_intensive(self):
        self.assertEqual(
            capex_intensity(-150, 1000),
            "Capital Intensive"
        )

    # -----------------------------
    # FCF Conversion
    # -----------------------------

    def test_fcf_conversion(self):
        self.assertEqual(
            fcf_conversion_rate(300, 400),
            75.0
        )

    def test_fcf_conversion_zero(self):
        self.assertIsNone(
            fcf_conversion_rate(300, 0)
        )

    # -----------------------------
    # Capital Allocation
    # -----------------------------

    def test_reinvestor(self):
        self.assertEqual(
            capital_allocation_pattern(
                100,
                -50,
                -20
            ),
            "Reinvestor"
        )

    def test_cash_accumulator(self):
        self.assertEqual(
            capital_allocation_pattern(
                100,
                20,
                50
            ),
            "Cash Accumulator"
        )

    def test_growth_debt(self):
        self.assertEqual(
            capital_allocation_pattern(
                -100,
                -50,
                200
            ),
            "Growth Funded by Debt"
        )


if __name__ == "__main__":
    unittest.main()