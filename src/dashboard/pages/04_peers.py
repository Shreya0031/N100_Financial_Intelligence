import streamlit as st

import plotly.graph_objects as go

from utils.db import (
    get_peer_group_names,
    get_peer_companies,
    get_peer_percentiles,
    get_peer_average_percentiles,
)

st.title("🤝 Peer Comparison")

# -------------------------------
# Peer Group
# -------------------------------

groups = get_peer_group_names()

selected_group = st.selectbox(
    "Select Peer Group",
    groups["peer_group_name"]
)

# -------------------------------
# Company
# -------------------------------

companies = get_peer_companies(selected_group)

selected_company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "company_id"
].iloc[0]

# -------------------------------
# Benchmark
# -------------------------------

benchmark = companies[
    companies["is_benchmark"] == 1
]

if not benchmark.empty:
    st.success(
        f"⭐ Benchmark Company: {benchmark.iloc[0]['company_name']}"
    )

st.divider()

# -------------------------------
# Peer Members
# -------------------------------

st.subheader("Peer Group Members")

peer_display = companies[
    ["company_name", "is_benchmark"]
].copy()

peer_display.columns = [
    "Company",
    "Benchmark"
]

peer_display["Benchmark"] = peer_display["Benchmark"].replace({
    1: "⭐ Benchmark",
    0: ""
})

st.dataframe(
    peer_display,
    use_container_width=True,
    hide_index=True
)

st.divider()


# -------------------------------
# Percentiles
# -------------------------------


st.subheader("Selected Company Percentiles")

percentiles = get_peer_percentiles(company_id)

st.dataframe(
    percentiles,
    use_container_width=True,
    hide_index=True
)

# ============================================
# Radar Chart
# ============================================

st.divider()

st.subheader("📊 Company vs Peer Average")

peer_avg = get_peer_average_percentiles(selected_group)

company_values = (
    percentiles
    .dropna(subset=["percentile_rank"])
    .set_index("metric")["percentile_rank"]
)

peer_values = (
    peer_avg
    .set_index("metric")["percentile_rank"]
)

# Keep only metrics that exist in both datasets
common_metrics = company_values.index.intersection(peer_values.index)

company_values = company_values.loc[common_metrics]
peer_values = peer_values.loc[common_metrics]

metric_names = {
    "asset_turnover": "Asset Turnover",
    "debt_to_equity": "Debt / Equity",
    "free_cash_flow_cr": "Free Cash Flow",
    "interest_coverage": "Interest Coverage",
    "net_profit_margin_pct": "Net Profit Margin",
    "return_on_equity_pct": "ROE"
}

metrics = [
    metric_names.get(metric, metric.replace("_", " ").title())
    for metric in common_metrics
]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=company_values.values,
    theta=metrics,
    fill="toself",
    name=selected_company
))

fig.add_trace(go.Scatterpolar(
    r=peer_values.reindex(metrics).values,
    theta=metrics,
    fill="toself",
    name="Peer Average"
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )
    ),
    showlegend=True,
    height=650
)

st.plotly_chart(
    fig,
    use_container_width=True
)