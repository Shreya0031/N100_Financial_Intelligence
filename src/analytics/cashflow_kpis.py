"""
Sprint 2 - Day 11
Cash Flow KPIs
"""


def free_cash_flow(operating_activity, investing_activity):
    """
    FCF = CFO + Investing Activity
    """
    return operating_activity + investing_activity


def cfo_quality_score(cfo, pat):
    """
    CFO / PAT Quality Score
    """
    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"
    elif ratio >= 0.5:
        return "Moderate"
    else:
        return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity %
    """
    if sales == 0:
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
    if operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)


def capital_allocation_pattern(cfo, cfi, cff):
    """
    Classify capital allocation pattern.
    """

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    patterns = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed"
    }

    return patterns.get(signs, "Unknown")

if __name__ == "__main__":
    print(free_cash_flow(500, -200))
    print(cfo_quality_score(300, 200))
    print(capex_intensity(-120, 1000))
    print(fcf_conversion_rate(300, 400))
    print(capital_allocation_pattern(100, -50, -20))