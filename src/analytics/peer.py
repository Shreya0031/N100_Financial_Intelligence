import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "db" / "nifty100.db"

# Load Data

def load_data():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT

        fr.company_id,
        fr.year,

        c.company_name,

        pg.peer_group_name,

        fr.return_on_equity_pct,
        fr.net_profit_margin_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,
        fr.interest_coverage,
        fr.asset_turnover,

        a.compounded_sales_growth,
        a.compounded_profit_growth

    FROM financial_ratios fr

    LEFT JOIN companies c
        ON fr.company_id = c.id

    LEFT JOIN peer_groups pg
    ON fr.company_id = pg.company_id

    LEFT JOIN (
    SELECT
        company_id,
        compounded_sales_growth,
        compounded_profit_growth
    FROM analysis
    WHERE compounded_sales_growth LIKE '5 Years%'
    ) a
    ON fr.company_id = a.company_id
    """

    df = pd.read_sql(query, conn)


    # Extract numeric percentage from text
    df["compounded_sales_growth"] = (
    df["compounded_sales_growth"]
    .astype(str)
    .str.extract(r"(-?\d+\.?\d*)")[0]
    )

    df["compounded_sales_growth"] = pd.to_numeric(
        df["compounded_sales_growth"],
        errors="coerce"
        )

    df["compounded_profit_growth"] = (
        df["compounded_profit_growth"]
        .astype(str)
        .str.extract(r"(-?\d+\.?\d*)")[0]
        )

    df["compounded_profit_growth"] = pd.to_numeric(
        df["compounded_profit_growth"],
        errors="coerce"
        )

    conn.close()

    df = (
        df.sort_values("year")
          .groupby("company_id", as_index=False)
          .last()
    )

    return df

#Percentile Calculation

def calculate_percentiles(df):

    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "free_cash_flow_cr",
        "compounded_sales_growth",
        "compounded_profit_growth",
        "interest_coverage",
        "asset_turnover"
    ]

    results = []

    for peer_group, group in df.groupby("peer_group_name", dropna=False):

        if pd.isna(peer_group):
            print("No peer group assigned")
            continue

        for metric in metrics:

            temp = group.copy()

            temp["percentile_rank"] = (
                temp[metric]
                .rank(pct=True)
                * 100
            ).round(2)

            temp["metric"] = metric
            temp["value"] = temp[metric]
            temp["peer_group_name"] = peer_group

            results.append(
                temp[
                    [
                        "company_id",
                        "peer_group_name",
                        "metric",
                        "value",
                        "percentile_rank",
                        "year"
                    ]
                ]
            )

        # Debt-to-Equity (lower is better)

        temp = group.copy()

        temp["percentile_rank"] = (
            1 - temp["debt_to_equity"].rank(pct=True)
        ) * 100

        temp["metric"] = "debt_to_equity"
        temp["value"] = temp["debt_to_equity"]
        temp["peer_group_name"] = peer_group

        results.append(
            temp[
                [
                    "company_id",
                    "peer_group_name",
                    "metric",
                    "value",
                    "percentile_rank",
                    "year"
                ]
            ]
        )

    return pd.concat(results, ignore_index=True)

# Save to SQLite

def save_percentiles(df):

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("\npeer_percentiles table created successfully.")
    print(f"Rows inserted : {len(df)}")


# Main Function
def main():

    df = load_data()

    print("Rows after load_data():", len(df))
    print(df[
        [
            "company_id",
            "company_name",
            "compounded_sales_growth",
            "compounded_profit_growth"
        ]
    ].head(20).to_string(index=False))

    percentile_df = calculate_percentiles(df)

    print("Rows in percentile_df:", len(percentile_df))

    save_percentiles(percentile_df)


if __name__ == "__main__":
    main()
