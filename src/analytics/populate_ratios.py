import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("=" * 60)
print("FINANCIAL RATIOS TABLE VERIFICATION")
print("=" * 60)

# Row count
count = cursor.execute(
    "SELECT COUNT(*) FROM financial_ratios"
).fetchone()[0]

print(f"Total Rows : {count}")

# Columns
columns = cursor.execute(
    "PRAGMA table_info(financial_ratios)"
).fetchall()

print("\nColumns:")

for col in columns:
    print(f"- {col[1]} ({col[2]})")

print("\nVerification Complete.")

conn.close()