import streamlit as st
import plotly.express as px

from utils.db import (
    get_metric_comparison,
    debug_metric,
)

st.title("📊 Company Metrics Comparison")

metric_map = {
    "Return on Equity (ROE)": "return_on_equity_pct",
    "Net Profit Margin": "net_profit_margin_pct",
    "Operating Profit Margin": "operating_profit_margin_pct",
    "Debt / Equity": "debt_to_equity",
    "Interest Coverage": "interest_coverage",
    "Asset Turnover": "asset_turnover",
    "Free Cash Flow": "free_cash_flow_cr",
}

selected_metric = st.selectbox(
    "Select Metric",
    list(metric_map.keys())
)

metric = metric_map[selected_metric]


# Fetch data
df = get_metric_comparison(metric)


# -----------------------------
# Rename Columns
# -----------------------------

display_df = df.rename(columns={
    "company_name": "Company",
    metric: selected_metric
})

# -----------------------------
# Ranking Table
# -----------------------------

st.subheader("📋 Company Ranking")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)