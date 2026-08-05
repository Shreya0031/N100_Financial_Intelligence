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


# ==========================================
# Sprint 5 - Cash Flow Intelligence
# ==========================================

from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)

cashflow = pd.read_sql("""
SELECT *
FROM cashflow
""", conn)

ratios = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

profit = pd.read_sql("""
SELECT *
FROM profitandloss
""", conn)

sectors = pd.read_sql("""
SELECT *
FROM sectors
""", conn)

# print("\n===== RAW PROFIT VBL =====")
# print(
#     profit.loc[
#         profit["company_id"] == "VBL",
#         ["company_id", "year"]
#     ]
# )


conn.close()

# ==========================================
# Normalize Year
# ==========================================

cashflow["year"] = (
    cashflow["year"]
    .astype(str)
    .str.extract(r"(\d{4})", expand=False)
)

ratios["year"] = (
    ratios["year"]
    .astype(str)
    .str.extract(r"(\d{4})", expand=False)
)

profit["year"] = (
    profit["year"]
    .astype(str)
    .str.extract(r"(\d{4})", expand=False)
)

# Remove rows like TTM that don't have a valid year
cashflow = cashflow.dropna(subset=["year"])
ratios = ratios.dropna(subset=["year"])
profit = profit.dropna(subset=["year"])

# ==========================================
# Latest Year Records
# ==========================================

cashflow = (
    cashflow.sort_values("year")
            .drop_duplicates("company_id", keep="last")
)

ratios = (
    ratios.sort_values("year")
          .drop_duplicates("company_id", keep="last")
)

profit = (
    profit.sort_values("year")
          .drop_duplicates("company_id", keep="last")
)

cashflow = cashflow.drop_duplicates(
    subset=["company_id", "year"]
)

ratios = ratios.drop_duplicates(
    subset=["company_id", "year"]
)

profit = profit.drop_duplicates(
    subset=["company_id", "year"]
)
# ==========================================
# Merge Tables
# ==========================================

df = ratios.merge(
    cashflow,
    on=["company_id", "year"],
    how="left"
)

df = df.merge(
    profit[
        [
            "company_id",
            "year",
            "sales",
            "operating_profit",
            "net_profit"
        ]
    ],
    on=["company_id", "year"],
    how="left"
)

df = df.merge(
    sectors[
        [
            "company_id",
            "broad_sector"
        ]
    ],
    on="company_id",
    how="left"
)

# ==========================================
# Cash Flow Intelligence KPIs
# ==========================================

df["cfo_quality_label"] = df.apply(
    lambda row: cfo_quality_score(
        row["cash_from_operations_cr"],
        row["net_profit"]
    ),
    axis=1
)

df["capex_label"] = df.apply(
    lambda row: capex_intensity(
        row["investing_activity"],
        row["sales"]
    ),
    axis=1
)

df["fcf_conversion_pct"] = df.apply(
    lambda row: fcf_conversion_rate(
        row["free_cash_flow_cr"],
        row["operating_profit"]
    ),
    axis=1
)

df["capital_allocation_label"] = df.apply(
    lambda row: capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    ),
    axis=1
)

# print(df.head())

# print(df.columns.tolist())

# print("Rows:", len(df))

# print("Cashflow rows:", len(cashflow))
# print("Cashflow companies:", cashflow["company_id"].nunique())

# print("Ratios rows:", len(ratios))
# print("Ratios companies:", ratios["company_id"].nunique())

# print("Profit rows:", len(profit))
# print("Profit companies:", profit["company_id"].nunique())

# print("Sectors rows:", len(sectors))
# print("Sectors companies:", sectors["company_id"].nunique())

# print("\n===== CASHFLOW VBL =====")
# print(cashflow[cashflow["company_id"].astype(str).str.strip() == "VBL"])

# print("\n===== PROFIT VBL =====")
# print(profit[profit["company_id"].astype(str).str.strip() == "VBL"])
# print("\n===== VBL YEAR VALUE =====")
# print(
#     profit.loc[
#         profit["company_id"].astype(str).str.strip() == "VBL",
#         ["year"]
#     ]
# )

# print("\n===== RATIOS VBL =====")
# print(ratios[ratios["company_id"].astype(str).str.strip() == "VBL"])

# print("\n===== SECTORS VBL =====")
# print(sectors[sectors["company_id"].astype(str).str.strip() == "VBL"])

# print("\n===== ABB Ratios =====")
# print(
#     ratios[
#         ratios["company_id"] == "ABB"
#     ][["company_id", "year"]].tail()
# )

# print("\n===== ABB Profit =====")
# print(
#     profit[
#         profit["company_id"] == "ABB"
#     ][["company_id", "year"]].tail()
# )

# print(df[
#     [
#         "company_id",
#         "cfo_quality_label",
#         "capex_label",
#         "fcf_conversion_pct",
#         "capital_allocation_label"
#     ]
# ].head())

# ==========================================
# Distress & Deleveraging Flags
# ==========================================

df["distress_flag"] = (
    (df["operating_activity"] < 0) &
    (df["financing_activity"] > 0)
)

df["deleveraging_flag"] = (
    (df["financing_activity"] < 0)
)

# ==========================================
# Final Output
# ==========================================

df["capex_intensity_pct"] = (
    abs(df["investing_activity"]) /
    df["sales"]
) * 100

output = df[
    [
        "company_id",
        "broad_sector",
        "cfo_quality_label",
        "capex_label",
        "fcf_conversion_pct",
        "distress_flag",
        "deleveraging_flag",
        "capital_allocation_label"
    ]
]

output.to_excel(
    OUTPUT_DIR / "cashflow_intelligence.xlsx",
    index=False
)

df[
    df["distress_flag"]
][
    [
        "company_id",
        "operating_activity",
        "financing_activity",
        "net_profit"
    ]
].to_csv(
    OUTPUT_DIR / "distress_alerts.csv",
    index=False
)

print("✅ cashflow_intelligence.xlsx generated")
print("✅ distress_alerts.csv generated")