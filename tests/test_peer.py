import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


def test_peer_percentiles_table():
    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM peer_percentiles")

    count = cur.fetchone()[0]

    conn.close()

    assert count > 0