"""
CAGR Engine
Sprint 2 - Day 10
"""

def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR and handle edge cases.

    Returns:
        (cagr_value, flag)
    """

    # Invalid period
    if years is None or years <= 0:
        return None, "INVALID_PERIOD"

    # Not enough historical data
    if years < 3:
        return None, "INSUFFICIENT_DATA"

    # Cannot calculate from zero
    if start_value is None or start_value == 0:
        return None, "ZERO_BASE"

    if end_value is None:
        return None, "INSUFFICIENT_DATA"

    # Normal CAGR
    if start_value > 0 and end_value > 0:
        cagr = ((end_value / start_value) ** (1 / years) - 1) * 100
        return round(cagr, 2), None

    # Profit → Loss
    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    # Loss → Profit
    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    # Loss → Loss
    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "INSUFFICIENT_DATA"


if __name__ == "__main__":
    test_cases = [
        (100, 200, 5),
        (100, -50, 5),
        (-100, 50, 5),
        (0, 100, 5),
        (100, 200, 2),
        (None, 100, 5),
    ]

    for case in test_cases:
        print(case, "->", calculate_cagr(*case))