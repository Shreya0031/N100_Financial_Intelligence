import sqlite3

conn = sqlite3.connect("db/nifty100.db")
cursor = conn.cursor()

print(cursor.execute("""
SELECT sql
FROM sqlite_master
WHERE type='table'
AND name='financial_ratios'
""").fetchone()[0])

conn.close()