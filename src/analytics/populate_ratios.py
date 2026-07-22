import sqlite3
import pandas as pd
from pathlib import Path

# ----------------------------------------------------
# Database
# ----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

print("Using DB:", DB_PATH.resolve())

conn = sqlite3.connect(DB_PATH)

# ----------------------------------------------------
# Load source tables
# ----------------------------------------------------

pl = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

bs = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cf = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

# ----------------------------------------------------
# Merge tables
# ----------------------------------------------------

df = (
    pl.merge(
        bs,
        on=["company_id", "year"],
        how="inner",
        suffixes=("", "_bs")
    )
    .merge(
        cf,
        on=["company_id", "year"],
        how="left",
        suffixes=("", "_cf")
    )
)

print("Merged Rows :", len(df))

# ----------------------------------------------------
# Replace missing values
# ----------------------------------------------------

numeric_cols = df.select_dtypes(include="number").columns

df[numeric_cols] = df[numeric_cols].fillna(0)

# ----------------------------------------------------
# Helper
# ----------------------------------------------------

def safe_div(a, b):
    if b == 0:
        return 0
    return a / b

# ----------------------------------------------------
# Calculate Equity
# ----------------------------------------------------

df["shareholders_equity"] = (
    df["equity_capital"] +
    df["reserves"]
)

# ----------------------------------------------------
# Financial Ratios
# ----------------------------------------------------

df["net_profit_margin_pct"] = df.apply(
    lambda r: safe_div(r["net_profit"], r["sales"]) * 100,
    axis=1
)

df["operating_profit_margin_pct"] = df.apply(
    lambda r: safe_div(r["operating_profit"], r["sales"]) * 100,
    axis=1
)

# Correct ROE
df["return_on_equity_pct"] = df.apply(
    lambda r: safe_div(
        r["net_profit"],
        r["shareholders_equity"]
    ) * 100,
    axis=1
)

df["debt_to_equity"] = df.apply(
    lambda r: safe_div(
        r["borrowings"],
        r["shareholders_equity"]
    ),
    axis=1
)

df["interest_coverage"] = df.apply(
    lambda r: safe_div(
        r["operating_profit"],
        r["interest"]
    ),
    axis=1
)

df["asset_turnover"] = df.apply(
    lambda r: safe_div(
        r["sales"],
        r["total_assets"]
    ),
    axis=1
)

df["free_cash_flow_cr"] = (
    df["operating_activity"] +
    df["investing_activity"]
)

df["capex_cr"] = (
    -df["investing_activity"]
)

df["earnings_per_share"] = df["eps"]

df["book_value_per_share"] = df.apply(
    lambda r: safe_div(
        r["shareholders_equity"],
        r["equity_capital"]
    ),
    axis=1
)

df["dividend_payout_ratio_pct"] = df["dividend_payout"]

df["total_debt_cr"] = df["borrowings"]

df["cash_from_operations_cr"] = df["operating_activity"]

print("Ratios Calculated Successfully")



# ----------------------------------------------------
# Keep only required columns
# ----------------------------------------------------

ratio_df = df[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr"
    ]
].copy()

# Round numeric values
numeric_cols = ratio_df.select_dtypes(include="number").columns
ratio_df[numeric_cols] = ratio_df[numeric_cols].round(2)

# ----------------------------------------------------
# Delete old ratios
# ----------------------------------------------------

cursor = conn.cursor()

cursor.execute("DELETE FROM financial_ratios")

conn.commit()

print("Old ratios deleted.")

# ----------------------------------------------------
# Insert new ratios
# ----------------------------------------------------

insert_sql = """
INSERT INTO financial_ratios (

company_id,
year,
net_profit_margin_pct,
operating_profit_margin_pct,
return_on_equity_pct,
debt_to_equity,
interest_coverage,
asset_turnover,
free_cash_flow_cr,
capex_cr,
earnings_per_share,
book_value_per_share,
dividend_payout_ratio_pct,
total_debt_cr,
cash_from_operations_cr

)

VALUES (

?,?,?,?,?,?,?,?,?,?,?,?,?,?,?

)
"""

cursor.executemany(
    insert_sql,
    ratio_df.values.tolist()
)

conn.commit()

print(f"{len(ratio_df)} rows inserted successfully!")

check = pd.read_sql("""
SELECT company_id, year, return_on_equity_pct
FROM financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10
""", conn)

print("\nTop ROE immediately after insert:")
print(check)

conn.close()

print("financial_ratios table rebuilt successfully.")