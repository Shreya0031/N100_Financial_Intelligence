from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

# List of required Excel files
DATASETS = {
    "companies": "companies.xlsx",
    "profitandloss": "profitandloss.xlsx",
    "balancesheet": "balancesheet.xlsx",
    "cashflow": "cashflow.xlsx",
    "analysis": "analysis.xlsx",
    "documents": "documents.xlsx",
    "prosandcons": "prosandcons.xlsx",
    "financial_ratios": "financial_ratios.xlsx",
    "market_cap": "market_cap.xlsx",
    "peer_groups": "peer_groups.xlsx",
    "sectors": "sectors.xlsx",
    "stock_prices": "stock_prices.xlsx"
}


def load_excel(file_path):
    """Load a single Excel file."""
    try:
        df = pd.read_excel(file_path, header=1)
        print(f"✓ Loaded {file_path.name}")
        return df

    except Exception as e:
        print(f"✗ Failed to load {file_path.name}")
        print(e)
        return None


def load_all_files():
    """Load all project datasets."""

    datasets = {}

    print("=" * 60)
    print("N100 FINANCIAL INTELLIGENCE PLATFORM")
    print("=" * 60)

    for name, filename in DATASETS.items():

        path = DATA_DIR / filename

        if not path.exists():
            print(f"Missing file: {filename}")
            continue

        df = load_excel(path)

        if df is not None:
            datasets[name] = df

            print(f"Rows    : {df.shape[0]}")
            print(f"Columns : {df.shape[1]}")
            print("-" * 40)

    print(f"\nSuccessfully loaded {len(datasets)} datasets.")

    return datasets


if __name__ == "__main__":
    load_all_files()