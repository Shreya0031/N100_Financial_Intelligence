from pathlib import Path
import sqlite3
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB = PROJECT_ROOT / "db" / "nifty100.db"

conn = sqlite3.connect(DB)

df = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 5",
    conn
)

print(df.columns.tolist())

conn.close()