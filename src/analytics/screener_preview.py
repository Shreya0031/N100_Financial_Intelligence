import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    fr.company_id,
    fr.year,
    fr.return_on_equity_pct,
    fr.debt_to_equity
FROM financial_ratios fr
JOIN (
    SELECT
        company_id,
        MAX(year) AS latest_year
    FROM financial_ratios
    GROUP BY company_id
) latest
ON fr.company_id = latest.company_id
AND fr.year = latest.latest_year
WHERE
    fr.return_on_equity_pct > 15
    AND fr.debt_to_equity < 1
ORDER BY fr.return_on_equity_pct DESC;
"""

df = pd.read_sql_query(query, conn)

print("=" * 70)
print("SCREENER PREVIEW")
print("=" * 70)

print(df.head(20))

print("\nTotal Companies Found:", len(df))

conn.close()