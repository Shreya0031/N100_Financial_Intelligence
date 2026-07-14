import sqlite3
import pandas as pd
from pathlib import Path

from cashflow_kpis import capital_allocation_pattern

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
OUTPUT_PATH = PROJECT_ROOT / "output" / "capital_allocation.csv"

conn = sqlite3.connect(DB_PATH)

cashflow = pd.read_sql_query(
    """
    SELECT
        company_id,
        year,
        operating_activity,
        investing_activity,
        financing_activity
    FROM cashflow
    """,
    conn
)

records = []

for _, row in cashflow.iterrows():

    cfo = row["operating_activity"]
    cfi = row["investing_activity"]
    cff = row["financing_activity"]

    records.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": "+" if cfo >= 0 else "-",
        "cfi_sign": "+" if cfi >= 0 else "-",
        "cff_sign": "+" if cff >= 0 else "-",
        "pattern_label": capital_allocation_pattern(cfo, cfi, cff)
    })

result = pd.DataFrame(records)

result.to_csv(OUTPUT_PATH, index=False)

print("✅ capital_allocation.csv generated")
print(result.head())

conn.close()