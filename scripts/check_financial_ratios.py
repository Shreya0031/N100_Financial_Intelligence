import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

df = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 5",
    conn
)

print("\nColumns:\n")
for col in df.columns:
    print(col)

conn.close()