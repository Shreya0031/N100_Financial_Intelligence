from openpyxl import load_workbook
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "nifty100.db"


def load_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        fr.*,

        c.company_name,

        s.broad_sector,
        s.sub_sector,

        p.sales,
        p.net_profit,

        a.compounded_sales_growth,
        a.compounded_profit_growth

    FROM financial_ratios fr

    LEFT JOIN companies c
        ON fr.company_id = c.id

    LEFT JOIN sectors s
        ON fr.company_id = s.company_id

    LEFT JOIN profitandloss p
        ON fr.company_id = p.company_id
        AND fr.year = p.year

    LEFT JOIN analysis a
        ON fr.company_id = a.company_id
    """

    df = pd.read_sql(query, conn)

    conn.close()

    df["company_name"] = (
        df["company_name"]
        .astype(str)
        .str.replace("\n", " ", regex=False)
        .str.strip()
    )

    df = (
        df.sort_values("year")
        .groupby("company_id", as_index=False)
        .last()
    )

    return df


def compare_company(df, company_name):

    company = df[
        df["company_name"]
        .str.contains(company_name, case=False, na=False)
    ]

    if company.empty:
        print("Company not found.")
        return

    sector = company.iloc[0]["broad_sector"]

    peers = df[
        df["broad_sector"] == sector
    ].copy()

    peers = peers.sort_values(
    by="composite_score",
    ascending=False
    )

    peers = peers.reset_index(drop=True)
    peers.insert(0, "Rank", peers.index + 1)

    display_df = peers[[
    "Rank",
    "company_name",
    "composite_score",
    "return_on_equity_pct",
    "debt_to_equity",
    "operating_profit_margin_pct",
    "free_cash_flow_cr",
    "sales",
    "net_profit"
    ]].copy()

    display_df.columns = [
    "Rank",
    "Company",
    "Score",
    "ROE %",
    "D/E",
    "OPM %",
    "FCF (Cr)",
    "Sales (Cr)",
    "PAT (Cr)"
    ]

    display_df = display_df.round(2)

    print("\nSector :", sector)
    print("\nPeer Companies\n")
    
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    print(display_df.to_string(index=False))

    export_peer_comparison(display_df, company_name)


def export_peer_comparison(display_df, company_name):
        
        output_path = BASE_DIR / "output" / "peer_comparison.xlsx"
        
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            display_df.to_excel(
                writer,
                sheet_name="Peer Comparison",
                index=False
                )
                
        print(f"\nPeer comparison exported successfully!")
        print(output_path)


def add_composite_score(df):

    df["compounded_sales_growth"] = pd.to_numeric(
        df["compounded_sales_growth"],
        errors="coerce"
    ).fillna(0)

    df["compounded_profit_growth"] = pd.to_numeric(
        df["compounded_profit_growth"],
        errors="coerce"
    ).fillna(0)

    df["debt_score"] = (
        1 / (1 + df["debt_to_equity"].fillna(0))
    ) * 100

    df["composite_score"] = (
          df["return_on_equity_pct"] * 0.25
        + df["compounded_sales_growth"] * 0.20
        + df["compounded_profit_growth"] * 0.20
        + df["operating_profit_margin_pct"] * 0.15
        + df["interest_coverage"] * 0.10
        + df["asset_turnover"] * 5
        + df["debt_score"] * 0.05
    ).round(2)

    return df


def main():

    df = load_data()
    df = add_composite_score(df)

    company = input("Enter Company Name : ")

    compare_company(df, company)


if __name__ == "__main__":
    main()
