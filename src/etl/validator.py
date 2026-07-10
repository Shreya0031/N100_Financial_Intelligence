from pathlib import Path
import pandas as pd

# ===============================
# Project Paths
# ===============================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

validation_results = []


# ===============================
# Helper Function
# ===============================
def log(rule, severity, table, issue):
    validation_results.append({
        "Rule": rule,
        "Severity": severity,
        "Table": table,
        "Issue": issue
    })


# ===============================
# Load Datasets
# ===============================
companies = pd.read_excel(DATA_DIR / "companies.xlsx", header=1)
profit = pd.read_excel(DATA_DIR / "profitandloss.xlsx", header=1)
balance = pd.read_excel(DATA_DIR / "balancesheet.xlsx", header=1)
cashflow = pd.read_excel(DATA_DIR / "cashflow.xlsx", header=1)
documents = pd.read_excel(DATA_DIR / "documents.xlsx", header=1)


# ======================================================
# DQ-01 Primary Key Uniqueness
# ======================================================
duplicates = companies["id"].duplicated().sum()

if duplicates == 0:
    print("✅ DQ-01 Passed")
else:
    log(
        "DQ-01",
        "CRITICAL",
        "companies",
        f"{duplicates} duplicate company IDs"
    )


# ======================================================
# DQ-02 Duplicate Company-Year
# ======================================================
duplicates = profit.duplicated(
    subset=["company_id", "year"]
).sum()

if duplicates == 0:
    print("✅ DQ-02 Passed")
else:
    log(
        "DQ-02",
        "CRITICAL",
        "profitandloss",
        f"{duplicates} duplicate company-year records"
    )


# ======================================================
# DQ-03 Foreign Key Integrity
# ======================================================
invalid_fk = ~profit["company_id"].isin(companies["id"])

if invalid_fk.sum() == 0:
    print("✅ DQ-03 Passed")
else:
    log(
        "DQ-03",
        "CRITICAL",
        "profitandloss",
        f"{invalid_fk.sum()} invalid foreign keys"
    )


# ======================================================
# DQ-04 Missing Values
# ======================================================
missing = profit.isnull().sum().sum()

if missing == 0:
    print("✅ DQ-04 Passed")
else:
    log(
        "DQ-04",
        "WARNING",
        "profitandloss",
        f"{missing} missing values"
    )


# ======================================================
# DQ-05 Duplicate Rows
# ======================================================
dup_rows = profit.duplicated().sum()

if dup_rows == 0:
    print("✅ DQ-05 Passed")
else:
    log(
        "DQ-05",
        "WARNING",
        "profitandloss",
        f"{dup_rows} duplicate rows"
    )


# ======================================================
# DQ-06 Positive Sales
# ======================================================
negative_sales = (profit["sales"] <= 0).sum()

if negative_sales == 0:
    print("✅ DQ-06 Passed")
else:
    log(
        "DQ-06",
        "CRITICAL",
        "profitandloss",
        f"{negative_sales} non-positive sales values"
    )


# ======================================================
# DQ-07 Balance Sheet Check
# ======================================================
difference = (
    balance["total_liabilities"] -
    balance["total_assets"]
).abs()

invalid_balance = (difference > 1).sum()

if invalid_balance == 0:
    print("✅ DQ-07 Passed")
else:
    log(
        "DQ-07",
        "WARNING",
        "balancesheet",
        f"{invalid_balance} balance sheet mismatches (>1)"
    )


# ======================================================
# DQ-08 Net Cash Flow
# ======================================================
missing_cash = cashflow["net_cash_flow"].isna().sum()

if missing_cash == 0:
    print("✅ DQ-08 Passed")
else:
    log(
        "DQ-08",
        "WARNING",
        "cashflow",
        f"{missing_cash} missing net cash flow values"
    )


# ======================================================
# DQ-09 Annual Report
# ======================================================
missing_reports = documents["Annual_Report"].isna().sum()

if missing_reports == 0:
    print("✅ DQ-09 Passed")
else:
    log(
        "DQ-09",
        "WARNING",
        "documents",
        f"{missing_reports} missing annual report links"
    )


# ======================================================
# DQ-10 Website URL
# ======================================================
missing_urls = companies["website"].isna().sum()

if missing_urls == 0:
    print("✅ DQ-10 Passed")
else:
    log(
        "DQ-10",
        "WARNING",
        "companies",
        f"{missing_urls} missing website URLs"
    )


# ======================================================
# Load remaining datasets
# ======================================================
analysis = pd.read_excel(DATA_DIR / "analysis.xlsx", header=1)
pros_cons = pd.read_excel(DATA_DIR / "prosandcons.xlsx", header=1)
ratios = pd.read_excel(DATA_DIR / "financial_ratios.xlsx")


# ======================================================
# DQ-11 Debt should not be negative
# ======================================================
negative_debt = (ratios["total_debt_cr"] < 0).sum()

if negative_debt == 0:
    print("✅ DQ-11 Passed")
else:
    log(
        "DQ-11",
        "WARNING",
        "financial_ratios",
        f"{negative_debt} negative debt values"
    )


# ======================================================
# DQ-12 Operating Cash Flow Missing
# ======================================================
missing_cfo = ratios["cash_from_operations_cr"].isna().sum()

if missing_cfo == 0:
    print("✅ DQ-12 Passed")
else:
    log(
        "DQ-12",
        "WARNING",
        "financial_ratios",
        f"{missing_cfo} missing operating cash flow values"
    )


# ======================================================
# DQ-13 Duplicate Pros & Cons
# ======================================================
dup_pc = pros_cons.duplicated().sum()

if dup_pc == 0:
    print("✅ DQ-13 Passed")
else:
    log(
        "DQ-13",
        "WARNING",
        "prosandcons",
        f"{dup_pc} duplicate records"
    )


# ======================================================
# DQ-14 Missing Pros
# ======================================================
missing_pros = pros_cons["pros"].isna().sum()

if missing_pros == 0:
    print("✅ DQ-14 Passed")
else:
    log(
        "DQ-14",
        "WARNING",
        "prosandcons",
        f"{missing_pros} missing pros"
    )


# ======================================================
# DQ-15 Missing Cons
# ======================================================
missing_cons = pros_cons["cons"].isna().sum()

if missing_cons == 0:
    print("✅ DQ-15 Passed")
else:
    log(
        "DQ-15",
        "WARNING",
        "prosandcons",
        f"{missing_cons} missing cons"
    )


# ======================================================
# DQ-16 Company Coverage
# ======================================================
missing_company = pros_cons["company_id"].isna().sum()

if missing_company == 0:
    print("✅ DQ-16 Passed")
else:
    log(
        "DQ-16",
        "CRITICAL",
        "prosandcons",
        f"{missing_company} missing company IDs"
    )

# ======================================================
# Save Validation Report
# ======================================================

report = pd.DataFrame(validation_results)

report.to_csv(
    OUTPUT_DIR / "validation_failures.csv",
    index=False
)

# ======================================================
# Summary
# ======================================================

total_rules = 16
failed_rules = len(report)
passed_rules = total_rules - failed_rules

print("\n" + "=" * 60)
print("DATA QUALITY VALIDATION REPORT")
print("=" * 60)

if report.empty:
    print("🎉 No validation failures found.")
else:
    print(report)

print("\nValidation Summary")
print("-" * 30)
print(f"Total Rules Checked : {total_rules}")
print(f"Passed              : {passed_rules}")
print(f"Failed              : {failed_rules}")
print(f"Report Saved        : {OUTPUT_DIR / 'validation_failures.csv'}")
print("=" * 60)