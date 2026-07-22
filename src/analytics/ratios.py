"""
Financial Ratio Engine
Sprint 2 - Day 08
"""

def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin = (Net Profit / Sales) * 100
    """
    if sales == 0 or sales is None:
        return None
    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin = (Operating Profit / Sales) * 100
    """
    if sales == 0 or sales is None:
        return None
    return round((operating_profit / sales) * 100, 2)


def return_on_equity(net_profit, equity_capital, reserves):
    """
    ROE = Net Profit / (Equity + Reserves) * 100
    """
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(ebit, equity_capital, reserves, borrowings):
    """
    ROCE = EBIT / (Equity + Reserves + Borrowings) * 100
    """
    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


def return_on_assets(net_profit, total_assets):
    """
    ROA = Net Profit / Total Assets * 100
    """
    if total_assets == 0 or total_assets is None:
        return None

    return round((net_profit / total_assets) * 100, 2)

if __name__ == "__main__":
    print("Net Profit Margin:", net_profit_margin(200, 1000))
    print("Operating Profit Margin:", operating_profit_margin(300, 1000))
    print("ROE:", return_on_equity(200, 500, 500))
    print("ROCE:", return_on_capital_employed(300, 500, 500, 200))
    print("ROA:", return_on_assets(200, 2500))

# ==========================================
# Debt-to-Equity Ratio
# ==========================================

def debt_to_equity(borrowings, equity_capital, reserves):
    equity = equity_capital + reserves

    if borrowings == 0:
        return 0

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


# ==========================================
# High Leverage Flag
# ==========================================

def high_leverage_flag(de_ratio, sector):
    if de_ratio is None:
        return False

    if sector.lower() == "financials":
        return False

    return de_ratio > 5


# ==========================================
# Interest Coverage Ratio
# ==========================================

def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio
    (Operating Profit + Other Income) / Interest
    """

    if interest is None or interest <= 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )


# ==========================================
# Interest Coverage Label
# ==========================================

def icr_label(interest):
    if interest == 0:
        return "Debt Free"

    return None


# ==========================================
# Interest Coverage Warning
# ==========================================

def icr_warning(icr):
    if icr is None:
        return False

    return icr < 1.5


# ==========================================
# Net Debt
# ==========================================

def net_debt(borrowings, investments):
    """
    Net Debt = Borrowings - Investments
    """

    borrowings = borrowings or 0
    investments = investments or 0

    return borrowings - investments
    
# ==========================================
# Asset Turnover
# ==========================================

def asset_turnover(sales, total_assets):
    """
    Asset Turnover Ratio
    """

    if total_assets is None or total_assets <= 0:
        return None

    return round(sales / total_assets, 2)

# ==========================================
# OPM Cross Validation
# ==========================================

def validate_opm(calculated_opm, source_opm):
    """
    Returns True if the difference between calculated OPM
    and source OPM is greater than 1%.
    """
    if calculated_opm is None or source_opm is None:
        return False

    return abs(calculated_opm - source_opm) > 1