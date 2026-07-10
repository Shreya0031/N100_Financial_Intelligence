import re
import pandas as pd


def normalize_year(value):
    """
    Normalize year values to a 4-digit integer.

    Examples:
        2024 -> 2024
        "2024" -> 2024
        "FY24" -> 2024
        "FY2024" -> 2024
    """

    if pd.isna(value):
        return None

    value = str(value).strip().upper()

    value = value.replace("FY", "")

    if len(value) == 2 and value.isdigit():
        return int("20" + value)

    if len(value) == 4 and value.isdigit():
        return int(value)

    digits = re.findall(r"\d{4}", value)

    if digits:
        return int(digits[0])

    return None


def normalize_ticker(value):
    """
    Normalize stock ticker symbols.

    Examples:
        " tcs " -> TCS
        "infy.ns" -> INFY
        " reliance " -> RELIANCE
    """

    if pd.isna(value):
        return None

    value = str(value).strip().upper()

    value = value.replace(".NS", "")
    value = value.replace(".BO", "")

    value = re.sub(r"[^A-Z0-9]", "", value)

    return value


if __name__ == "__main__":

    print(normalize_year("FY24"))
    print(normalize_year("2025"))
    print(normalize_year("FY2026"))

    print(normalize_ticker(" tcs "))
    print(normalize_ticker("infy.ns"))
    print(normalize_ticker(" reliance "))