import sqlite3
import pandas as pd
from pathlib import Path

# ===========================
# Paths
# ===========================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB = PROJECT_ROOT / "db" / "nifty100.db"
OUTPUT = PROJECT_ROOT / "output"

OUTPUT.mkdir(exist_ok=True)

# ===========================
# Connect
# ===========================
conn = sqlite3.connect(DB)

ratios = pd.read_sql("""
SELECT *
FROM financial_ratios
""", conn)

profit = pd.read_sql("""
SELECT *
FROM profitandloss
""", conn)

companies = pd.read_sql("""
SELECT *
FROM companies
""", conn)

conn.close()

# ===========================
# Latest Year Data
# ===========================
ratios = (
    ratios.sort_values("year")
          .drop_duplicates("company_id", keep="last")
)

profit = (
    profit.sort_values("year")
          .drop_duplicates("company_id", keep="last")
)

df = ratios.merge(
    profit[
        [
            "company_id",
            "opm_percentage",
            "net_profit"
        ]
    ],
    on="company_id",
    how="left"
)

df = df.merge(
    companies[
        [
            "id",
            "roce_percentage"
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left"
)

records = []

# ===========================
# Rule Engine
# ===========================
for _, row in df.iterrows():

    company = row["company_id"]

    # -----------------------
    # Rule P1
    # -----------------------
    if row["return_on_equity_pct"] > 20:

        records.append({

            "company_id": company,
            "type": "Pro",
            "rule_id": "P1",
            "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
            "confidence_pct": 90

        })

    # -----------------------
    # Rule P2
    # -----------------------
    if row["free_cash_flow_cr"] > 0:

        records.append({

            "company_id": company,
            "type": "Pro",
            "rule_id": "P2",
            "text": "Strong free cash flow generation signals healthy business fundamentals.",
            "confidence_pct": 85

        })

    # -----------------------
    # Rule P3
    # -----------------------
    if row["debt_to_equity"] == 0:

        records.append({

            "company_id": company,
            "type": "Pro",
            "rule_id": "P3",
            "text": "Debt-free balance sheet provides excellent financial flexibility.",
            "confidence_pct": 95

        })

    # -----------------------
    # Rule P5
    # -----------------------
    if row["opm_percentage"] > 25:

        records.append({

            "company_id": company,
            "type": "Pro",
            "rule_id": "P5",
            "text": "Operating profit margin above 25% indicates strong pricing power.",
            "confidence_pct": 88

        })


    # -----------------------
    # Rule C1
    # -----------------------
    if row["debt_to_equity"] > 2:
        
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C1",
            "text": f"Debt-to-equity ratio of {row['debt_to_equity']:.2f} is elevated and warrants monitoring.",
            "confidence_pct": 90
        })

    # -----------------------
    # Rule C4
    # -----------------------
    if row["net_profit"] < 0:
         records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C4",
            "text": "Company reported a net loss in the most recent financial year.",
            "confidence_pct": 95
          })

    # -----------------------
    # Rule C6
    # -----------------------
    if row["interest_coverage"] < 1.5:

        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C6",
            "text": "Interest coverage ratio below 1.5 indicates elevated debt servicing risk.",
            "confidence_pct": 90
        })
    
    # -----------------------
    # Rule C7
    # -----------------------
    if row["dividend_payout_ratio_pct"] > 100:
        
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C7",
            "text": "Dividend payout ratio above 100% may be difficult to sustain.",
            "confidence_pct": 85
        })

    # -----------------------
    # Rule C10
    # -----------------------
    if row["roce_percentage"] < 10:
        
        records.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C10",
            "text": "Return on capital employed below 10% suggests weaker capital efficiency.",
            "confidence_pct": 80
    })

# ===========================
# Save
# ===========================
pros_cons = pd.DataFrame(records)

pros_cons.to_csv(
    OUTPUT / "pros_cons_generated.csv",
    index=False
)

print("===================================")
print("Pros & Cons Generated")
print("===================================")
print(pros_cons.head())
print()
print("Total Rules Generated:", len(pros_cons))