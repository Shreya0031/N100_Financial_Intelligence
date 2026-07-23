from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "reports" / "radar_charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_data():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql("""
        SELECT
            company_id,
            peer_group_name,
            metric,
            percentile_rank
        FROM peer_percentiles
    """, conn)

    conn.close()

    return df

def prepare_data(df):

    radar = df.pivot_table(
        index=["company_id", "peer_group_name"],
        columns="metric",
        values="percentile_rank"
    ).reset_index()

    return radar

METRICS = [
    "return_on_equity_pct",
    "net_profit_margin_pct",
    "free_cash_flow_cr",
    "compounded_sales_growth",
    "compounded_profit_growth",
    "interest_coverage",
    "asset_turnover",
    "debt_to_equity"
]


def create_radar_chart(row, peer_average):

    values = []

    for metric in METRICS:
        values.append(row.get(metric, 0))

    values = np.nan_to_num(values, nan=0)

    values = np.append(values, values[0])

    peer_values = []
    
    for metric in METRICS:
        peer_values.append(peer_average.get(metric, 0))

    peer_values = np.nan_to_num(peer_values, nan=0)
    peer_values = np.append(peer_values, peer_values[0])

    angles = np.linspace(
        0,
        2 * np.pi,
        len(METRICS),
        endpoint=False
    )

    angles = np.append(angles, angles[0])

    fig = plt.figure(figsize=(8, 8))

    ax = plt.subplot(111, polar=True)

    # Company
    ax.plot(
        angles,
        values,
        linewidth=2,
        label="Company"
        )
        
    # Peer Average
    ax.plot(
        angles,
        peer_values,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
        )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels([
        "ROE",
        "NPM",
        "FCF",
        "Sales CAGR",
        "Profit CAGR",
        "Interest",
        "Asset Turn",
        "D/E"
    ])

    ax.set_title(
        row["company_id"],
        fontsize=14,
        pad=20
    )

    ax.legend(loc="upper right")

    plt.savefig(
        OUTPUT_DIR / f"{row['company_id']}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

def main():

    df = load_data()

    radar = prepare_data(df)

    print(f"Companies : {len(radar)}")

    for _, row in radar.iterrows():
        
        peer_average = (
            radar[radar["peer_group_name"] == row["peer_group_name"]]
            [METRICS]
            .mean()
            )
            
        create_radar_chart(row, peer_average)

    print(f"Radar charts saved to:\n{OUTPUT_DIR}")


if __name__ == "__main__":
    main()