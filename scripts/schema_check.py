from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

df = pd.read_excel(DATA_DIR / "market_cap.xlsx", header=0)

print(df.columns.tolist())