import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(r"E:\N100_Financial_Intelligence\db\nifty100.db")

print("Using DB:", DB_PATH.resolve())

conn = sqlite3.connect(DB_PATH)

# Total rows
count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM financial_ratios",
    conn
)
print("\nRow Count:")
print(count)

# Check top ROE values
query = """
SELECT
    company_id,
    year,
    return_on_equity_pct
FROM financial_ratios
ORDER BY return_on_equity_pct DESC
LIMIT 10;
"""

df = pd.read_sql(query, conn)

print("\nTop ROE:")
print(df)

conn.close()