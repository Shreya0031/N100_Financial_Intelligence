import sqlite3
import pandas as pd

conn = sqlite3.connect(r"E:\N100_Financial_Intelligence\db\nifty100.db")

print(pd.read_sql(
    "SELECT DISTINCT metric FROM peer_percentiles",
    conn
))

conn.close()