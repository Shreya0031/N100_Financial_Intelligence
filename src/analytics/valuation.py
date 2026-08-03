import sqlite3
import pandas as pd
from pathlib import Path

# -----------------------------
# Project Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# -----------------------------
# Connect Database
# -----------------------------
conn = sqlite3.connect(DB_PATH)

# -----------------------------
# Load Tables
# -----------------------------
companies = pd.read_sql("SELECT * FROM companies", conn)

sectors = pd.read_sql("SELECT * FROM sectors", conn)

print(sectors.columns.tolist())
print(sectors.head())

print(companies.columns.tolist())

ratios = pd.read_sql("""
SELECT
company_id,
year,
free_cash_flow_cr
FROM financial_ratios
""", conn)

market = pd.read_sql("""
SELECT
company_id,
year,
market_cap_crore,
pe_ratio,
pb_ratio,
ev_ebitda
FROM market_cap
""", conn)

conn.close()

print("\nAfter conversion:")
print(ratios.dtypes)
print(market.dtypes)

print(ratios.head())
print(market.head())

# Extract year from financial_ratios
ratios["year"] = (
    ratios["year"]
    .astype(str)
    .str.extract(r"(\d{4})", expand=False)
)

# Convert market year to string
market["year"] = market["year"].astype(str)

# Keep only one record per company-year
ratios = (
    ratios
    .sort_values(["company_id", "year"])
    .drop_duplicates(
        subset=["company_id", "year"],
        keep="first"
    )
)

# -----------------------------
# Merge
# -----------------------------
df = market.merge(
    ratios,
    on=["company_id", "year"],
    how="left"
)

# Add company name
df = df.merge(
    companies[["id", "company_name"]],
    left_on="company_id",
    right_on="id",
    how="left"
)

# Add sector information
df = df.merge(
    sectors[["company_id", "broad_sector"]],
    on="company_id",
    how="left"
)

# Rename broad_sector -> sector
df.rename(
    columns={"broad_sector": "sector"},
    inplace=True
)

# -----------------------------
# FCF Yield
# -----------------------------
df["FCF_yield_pct"] = (
    df["free_cash_flow_cr"] /
    df["market_cap_crore"]
) * 100

# -----------------------------
# Sector Median PE
# -----------------------------
sector_pe = (
    df.groupby("sector")["pe_ratio"]
      .median()
      .reset_index()
)

sector_pe.rename(
    columns={
        "pe_ratio": "sector_median_pe"
    },
    inplace=True
)

df = df.merge(
    sector_pe,
    on="sector",
    how="left"
)

# -----------------------------
# PE vs Sector Median
# -----------------------------
df["PE_vs_sector_median_pct"] = (
    df["pe_ratio"] /
    df["sector_median_pe"]
) * 100

# -----------------------------
# Flag
# -----------------------------
def valuation_flag(row):

    if row["pe_ratio"] > row["sector_median_pe"] * 1.5:
        return "Caution"

    elif row["pe_ratio"] < row["sector_median_pe"] * 0.7:
        return "Discount"

    else:
        return "Fair"


df["flag"] = df.apply(
    valuation_flag,
    axis=1
)

# -----------------------------
# Final Columns
# -----------------------------
summary = df[
    [
        "company_id",
        "company_name",
        "sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "FCF_yield_pct",
        "sector_median_pe",
        "PE_vs_sector_median_pct",
        "flag"
    ]
]

# -----------------------------
# Save Files
# -----------------------------
summary.to_excel(
    OUTPUT_DIR / "valuation_summary.xlsx",
    index=False
)

summary[
    summary["flag"] != "Fair"
].to_csv(
    OUTPUT_DIR / "valuation_flags.csv",
    index=False
)

print("✅ valuation_summary.xlsx generated")
print("✅ valuation_flags.csv generated")