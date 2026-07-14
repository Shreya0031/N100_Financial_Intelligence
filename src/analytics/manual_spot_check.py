import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
DATA_DIR = PROJECT_ROOT / "data"

conn = sqlite3.connect(DB_PATH)

companies = ["TCS", "ABB", "INFY"]

print("=" * 70)
print("MANUAL SPOT CHECK")
print("=" * 70)

for company in companies:

    print(f"\nCompany : {company}")

    db = pd.read_sql_query(
        f"""
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            net_profit_margin_pct,
            debt_to_equity
        FROM financial_ratios
        WHERE company_id='{company}'
        LIMIT 5
        """,
        conn,
    )

    print(db)

conn.close()