"""
Sprint 2 - Day 11
Cash Flow KPIs
"""


def free_cash_flow(operating_activity, investing_activity):
    """
    FCF = Cash Flow from Operations + Cash Flow from Investing
    """

    operating_activity = operating_activity or 0
    investing_activity = investing_activity or 0

    return operating_activity + investing_activity


def cfo_quality_score(cfo, pat):
    """
    CFO/PAT Quality Score
    """

    if pat is None or pat == 0:
        return None

    ratio = cfo / pat

    if ratio >= 1:
        return "High Quality"
    elif ratio >= 0.5:
        return "Moderate"
    else:
        return "Accrual Risk"

def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity Classification
    """

    if sales is None or sales <= 0:
        return None

    value = abs(investing_activity) / sales * 100

    if value < 3:
        return "Asset Light"
    elif value <= 8:
        return "Moderate"
    else:
        return "Capital Intensive"


def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion %
    """

    if operating_profit is None or operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)


def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):
    """
    Classify capital allocation pattern.
    """

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    if signs == ("+", "-", "-"):
        if cfo_pat_ratio is not None and cfo_pat_ratio >= 1:
            return "Shareholder Returns"
        return "Reinvestor"

    patterns = {
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed"
    }

    return patterns.get(signs, "Unknown")

if __name__ == "__main__":
    print("FCF:", free_cash_flow(500, -200))
    print("CFO Quality:", cfo_quality_score(300, 200))
    print("CapEx:", capex_intensity(-120, 1000))
    print("FCF Conversion:", fcf_conversion_rate(300, 400))
    print("Pattern:", capital_allocation_pattern(100, -50, -20, 1.2))