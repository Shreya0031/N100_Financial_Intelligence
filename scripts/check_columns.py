import pandas as pd

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx"
]

for file in files:
    df = pd.read_excel(f"data/{file}")
    print(f"\n{file}")
    print(df.columns.tolist())