import sqlite3
import pandas as pd
import yaml
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "db" / "nifty100.db"
CONFIG_PATH = BASE_DIR / "config" / "screener_config.yaml"


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

    # Clean company names AFTER df exists
    df["company_name"] = (
    df["company_name"]
      .astype(str)
      .str.replace("\n", " ", regex=False)
      .str.replace(r"\s+", " ", regex=True)
      .str.strip()
      )


    # Keep only the latest year for each company
    df = (
        df.sort_values("year")
        .groupby("company_id", as_index=False)
        .last()
        )

    conn.close()

    return df

def load_config():
    with open(CONFIG_PATH, "r") as file:
        config = yaml.safe_load(file)

    return config["filters"]

def apply_filters(df, filters):

    # ROE
    if filters.get("roe_min") is not None:
        df = df[df["return_on_equity_pct"] >= filters["roe_min"]]

    # Debt to Equity
    if filters.get("debt_to_equity_max") is not None:

        mask = (
            (df["broad_sector"] == "Financials") |
            (df["debt_to_equity"] <= filters["debt_to_equity_max"])
        )

        df = df[mask]

    # Free Cash Flow
    if filters.get("free_cash_flow_min") is not None:
        df = df[df["free_cash_flow_cr"] >= filters["free_cash_flow_min"]]

    # Revenue Growth
    if filters.get("revenue_cagr_5yr_min") is not None:
        df = df[
            df["compounded_sales_growth"] >=
            filters["revenue_cagr_5yr_min"]
        ]

    # Profit Growth
    if filters.get("pat_cagr_5yr_min") is not None:
        df = df[
            df["compounded_profit_growth"] >=
            filters["pat_cagr_5yr_min"]
        ]

    # Operating Margin
    if filters.get("operating_profit_margin_min") is not None:
        df = df[
            df["operating_profit_margin_pct"] >=
            filters["operating_profit_margin_min"]
        ]

    # Interest Coverage
    if filters.get("interest_coverage_min") is not None:

        df = df[
            (df["interest_coverage"].isna()) |
            (df["interest_coverage"] >=
             filters["interest_coverage_min"])
        ]

    # Asset Turnover
    if filters.get("asset_turnover_min") is not None:
        df = df[
            df["asset_turnover"] >=
            filters["asset_turnover_min"]
        ]

    # Sales
    if filters.get("sales_min") is not None:
        df = df[
            df["sales"] >=
            filters["sales_min"]
        ]

    # Net Profit
    if filters.get("net_profit_min") is not None:
        df = df[
            df["net_profit"] >=
            filters["net_profit_min"]
        ]

    return df



def sort_results(df):

    if "composite_score" in df.columns:

        return df.sort_values(
            by="composite_score",
            ascending=False
        )

    return df

def quality_compounder(df):
    return df[
        (df["return_on_equity_pct"] > 15) &
        (df["debt_to_equity"] < 1) &
        (df["free_cash_flow_cr"] > 0)
    ]


def value_pick(df):
    return df[
        (df["debt_to_equity"] < 1.5) &
        (df["dividend_payout_ratio_pct"] > 10)
    ]


def growth_accelerator(df):

    return df[
        (df["return_on_equity_pct"] > 18) &
        (df["operating_profit_margin_pct"] > 15) &
        (df["free_cash_flow_cr"] > 0)
    ]


def dividend_champion(df):
    return df[
        (df["dividend_payout_ratio_pct"] > 20) &
        (df["dividend_payout_ratio_pct"] < 80) &
        (df["free_cash_flow_cr"] > 0)
    ]


def debt_free_bluechip(df):

    return df[
        (df["debt_to_equity"] == 0) &
        (df["return_on_equity_pct"] > 12) &
        (df["sales"] > 5000)
    ]


def turnaround_watch(df):
    return df[
        (df["free_cash_flow_cr"] > 0) &
        (df["operating_profit_margin_pct"] > 15)
    ]


def export_to_excel(presets):

    output_path = BASE_DIR / "output" / "screener_output.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        for name, df in presets.items():

            export_df = df.copy()

            export_df["company_name"] = (
                export_df["company_name"]
                .astype(str)
                .str.replace("\n", " ", regex=False)
                .str.replace(r"\s+", " ", regex=True)
                .str.strip()
            )

            # Keep only useful columns
            columns = [
                "company_name",
                "broad_sector",
                "sub_sector",
                "year",
                "return_on_equity_pct",
                "debt_to_equity",
                "operating_profit_margin_pct",
                "interest_coverage",
                "asset_turnover",
                "free_cash_flow_cr",
                "sales",
                "net_profit",
                "earnings_per_share",
                "book_value_per_share",
                "dividend_payout_ratio_pct",
                "composite_score"
            ]

            export_df = export_df[columns]

            # Sort by ROE
            export_df = sort_results(export_df)

            export_df.to_excel(
                writer,
                sheet_name=name[:31],
                index=False
            )

    print("\nExcel exported successfully!")
    print(output_path)


    export_df = export_df.sort_values(
    by="return_on_equity_pct",
    ascending=False
    )


def add_composite_score(df):

    # Convert CAGR columns to numeric
    df["compounded_sales_growth"] = pd.to_numeric(
        df["compounded_sales_growth"],
        errors="coerce"
    ).fillna(0)

    df["compounded_profit_growth"] = pd.to_numeric(
        df["compounded_profit_growth"],
        errors="coerce"
    ).fillna(0)

    # Lower debt is better
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

    presets = {
        "Quality Compounder": quality_compounder(df),
        "Value Pick": value_pick(df),
        "Growth Accelerator": growth_accelerator(df),
        "Dividend Champion": dividend_champion(df),
        "Debt-Free Blue Chip": debt_free_bluechip(df),
        "Turnaround Watch": turnaround_watch(df)
    }

    for name, result in presets.items():

        print("\n" + "=" * 60)
        print(name)
        print(f"Companies Found: {len(result)}")

        if not result.empty:
            print(
                result[
                    [
                        "company_name",
                        "return_on_equity_pct",
                        "debt_to_equity",
                        "free_cash_flow_cr",
                        "sales"
                    ]
                ].head(10)
            )
        else:
            print("No companies found.")

    export_to_excel(presets)



if __name__ == "__main__":
    main()