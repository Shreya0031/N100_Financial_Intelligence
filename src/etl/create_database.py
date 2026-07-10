from pathlib import Path
import sqlite3
import pandas as pd

# =====================================
# Project Paths
# =====================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
DB_DIR = PROJECT_ROOT / "db"

DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "nifty100.db"
SCHEMA_PATH = DB_DIR / "schema.sql"

# =====================================
# Create Database
# =====================================
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Enable Foreign Keys
cursor.execute("PRAGMA foreign_keys = ON;")

# Execute schema.sql
with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
    cursor.executescript(file.read())

print("✅ Database schema created.")

# =====================================
# Load Excel Files
# =====================================

datasets = {
    "companies": ("companies.xlsx", 1),
    "profitandloss": ("profitandloss.xlsx", 1),
    "balancesheet": ("balancesheet.xlsx", 1),
    "cashflow": ("cashflow.xlsx", 1),
    "analysis": ("analysis.xlsx", 1),
    "documents": ("documents.xlsx", 1),
    "prosandcons": ("prosandcons.xlsx", 1),
    "financial_ratios": ("financial_ratios.xlsx", 0),
    "peer_groups": ("peer_groups.xlsx", 1),
    "stock_prices": ("stock_prices.xlsx", 1),
    "sectors": ("sectors.xlsx", 0)
}

audit = []

for table, (filename, header_row) in datasets.items():

    file_path = DATA_DIR / filename

    try:

        df = pd.read_excel(file_path, header=header_row)

        df.to_sql(
            table,
            conn,
            if_exists="replace",
            index=False
        )

        audit.append({
            "table": table,
            "rows_loaded": len(df),
            "status": "SUCCESS"
        })

        print(f"✅ Loaded {table:<20} {len(df)} rows")

    except Exception as e:

        audit.append({
            "table": table,
            "rows_loaded": 0,
            "status": str(e)
        })

        print(f"❌ {table} -> {e}")

# =====================================
# Save Load Audit
# =====================================

audit_df = pd.DataFrame(audit)

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

audit_df.to_csv(
    OUTPUT_DIR / "load_audit.csv",
    index=False
)

print("\n======================================")
print("Database Created Successfully")
print(f"Database : {DB_PATH}")
print("Load Audit Saved")
print("======================================")

conn.close()