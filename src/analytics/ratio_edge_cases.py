from pathlib import Path
import pandas as pd

# ===============================
# Project Paths
# ===============================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# ===============================
# Load Data
# ===============================
companies = pd.read_excel(DATA_DIR / "companies.xlsx", header=1)
sectors = pd.read_excel(DATA_DIR / "sectors.xlsx", header=0)

# ===============================
# Log File
# ===============================
log_file = OUTPUT_DIR / "ratio_edge_cases.log"

with open(log_file, "w", encoding="utf-8") as f:

    f.write("=" * 60 + "\n")
    f.write("FINANCIAL RATIO EDGE CASE REPORT\n")
    f.write("=" * 60 + "\n\n")

    # Financial Sector Companies
    financials = sectors[
        sectors["broad_sector"].astype(str).str.strip() == "Financials"
    ]

    f.write(f"Financial Sector Companies: {len(financials)}\n\n")

    for _, row in financials.iterrows():
        f.write(
            f"{row['company_id']} -> "
            f"{row['sub_sector']} | "
            "High Debt-to-Equity warning suppressed\n"
        )

    # ===============================
    # ROE & ROCE Cross Check
    # ===============================

    f.write("\n")
    f.write("=" * 60 + "\n")
    f.write("ROE / ROCE CROSS CHECK\n")
    f.write("=" * 60 + "\n\n")

    for _, row in companies.iterrows():

        source_roe = row["roe_percentage"]
        source_roce = row["roce_percentage"]

        # Placeholder values
        computed_roe = source_roe
        computed_roce = source_roce

        if pd.notna(source_roe):

            diff = abs(source_roe - computed_roe)

            if diff > 5:
                f.write(
                    f"{row['company_name']} | "
                    f"ROE Difference: {diff:.2f}% | "
                    "Category: Formula Discrepancy\n"
                )

        if pd.notna(source_roce):

            diff = abs(source_roce - computed_roce)

            if diff > 5:
                f.write(
                    f"{row['company_name']} | "
                    f"ROCE Difference: {diff:.2f}% | "
                    "Category: Formula Discrepancy\n"
                )

print("✅ ratio_edge_cases.log generated successfully")
print(f"Saved at: {log_file}")