from pathlib import Path
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("=" * 50)
print("TABLES IN DATABASE")
print("=" * 50)

for table in tables:
    print(table[0])

print("\n" + "=" * 50)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    rows = cursor.fetchone()[0]
    print(f"{table[0]:20} {rows}")

conn.close()