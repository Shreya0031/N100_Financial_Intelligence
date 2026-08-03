import streamlit as st
import plotly.express as px

from utils.db import get_capital_metrics

st.title("💰 Capital Allocation Dashboard")

df = get_capital_metrics()

# -----------------------------
# KPI Cards
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average ROE",
    f"{df['return_on_equity_pct'].mean():.2f}"
)

col2.metric(
    "Average Debt/Equity",
    f"{df['debt_to_equity'].mean():.2f}"
)

col3.metric(
    "Average Asset Turnover",
    f"{df['asset_turnover'].mean():.2f}"
)

col4.metric(
    "Average Interest Coverage",
    f"{df['interest_coverage'].mean():.2f}"
)

st.divider()

# -----------------------------
# Capital Metrics Table
# -----------------------------

st.subheader("Capital Allocation Metrics")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# ROE Chart
# -----------------------------

st.divider()

st.subheader("Top 10 Companies by ROE")

top10 = (
    df.sort_values(
        "return_on_equity_pct",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top10,
    x="company_name",
    y="return_on_equity_pct",
    color="return_on_equity_pct",
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Debt vs ROE
# -----------------------------

st.divider()

st.subheader("Debt to Equity vs ROE")

fig2 = px.scatter(
    df,
    x="debt_to_equity",
    y="return_on_equity_pct",
    hover_name="company_name",
)

st.plotly_chart(
    fig2,
    use_container_width=True
)