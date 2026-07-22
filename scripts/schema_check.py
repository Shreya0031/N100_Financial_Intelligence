import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.execute("PRAGMA table_info(analysis)")

print("Columns in analysis:\n")

for row in cursor.fetchall():
    print(row)

conn.close()