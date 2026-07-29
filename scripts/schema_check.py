import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

print("=== peer_percentiles ===")
for row in conn.execute("PRAGMA table_info(peer_percentiles)"):
    print(row)

conn.close()