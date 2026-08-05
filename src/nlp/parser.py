import sqlite3
import pandas as pd
import re
from pathlib import Path

# =====================================
# Project Paths
# =====================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# =====================================
# Connect Database
# =====================================
conn = sqlite3.connect(DB_PATH)

analysis = pd.read_sql(
    "SELECT * FROM analysis",
    conn
)

conn.close()

# =====================================
# Regex Pattern
# =====================================

pattern = re.compile(
    r"(\d+)\s*Years?:?\s*([\-\d.]+)%"
)

parsed = []
failures = []

columns = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe"
]

# =====================================
# Parse Analysis Text
# =====================================

for _, row in analysis.iterrows():

    company = row["company_id"]

    for metric in columns:

        value = row[metric]

        if pd.isna(value):
            continue

        text = str(value)

        match = pattern.search(text)

        if match:

            parsed.append({

                "company_id": company,
                "metric_type": metric,
                "period_years": int(match.group(1)),
                "value_pct": float(match.group(2))

            })

        else:

            failures.append({

                "company_id": company,
                "metric_type": metric,
                "raw_text": text

            })

# =====================================
# Save Outputs
# =====================================

parsed_df = pd.DataFrame(parsed)

fail_df = pd.DataFrame(failures)

parsed_df.to_csv(
    OUTPUT_DIR / "analysis_parsed.csv",
    index=False
)

fail_df.to_csv(
    OUTPUT_DIR / "parse_failures.csv",
    index=False
)

print("✅ analysis_parsed.csv generated")
print("✅ parse_failures.csv generated")

print(f"Parsed Records : {len(parsed_df)}")
print(f"Failures       : {len(fail_df)}")