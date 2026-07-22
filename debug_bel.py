import sqlite3
import pandas as pd

conn = sqlite3.connect(r"E:\N100_Financial_Intelligence\db\nifty100.db")

query = """
SELECT
    p.company_id,
    p.year,
    p.sales,
    p.net_profit,
    b.equity_capital,
    b.reserves,
    b.borrowings,
    b.total_assets
FROM profitandloss p
JOIN balancesheet b
ON p.company_id = b.company_id
AND p.year = b.year
WHERE p.company_id = 'BEL'
AND p.year = 'Mar 2024';
"""

df = pd.read_sql(query, conn)

print(df.to_string(index=False))

conn.close()