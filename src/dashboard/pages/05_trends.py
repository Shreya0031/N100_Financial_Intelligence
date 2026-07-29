import streamlit as st
import plotly.express as px

from utils.db import (
    get_company_list,
    get_trend_data,
    get_roe_trend,
)

st.title("📈 Financial Trends")

companies = get_company_list()

selected_company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "id"
].iloc[0]

trend_data = get_trend_data(company_id)
roe_data = get_roe_trend(company_id)


# -------------------------------
# Latest Financial Summary
# -------------------------------

latest = trend_data.iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Revenue",
    f"₹ {latest['sales']:,} Cr"
)

col2.metric(
    "Net Profit",
    f"₹ {latest['net_profit']:,} Cr"
)

col3.metric(
    "OPM",
    f"{latest['opm_percentage']}%"
)


st.divider()

st.subheader("📈 Revenue Trend")

fig = px.line(
    trend_data,
    x="year",
    y="sales",
    markers=True
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Sales (₹ Cr)",
    height=450,
    template="plotly_dark",
    hovermode="x unified"
)

fig.update_xaxes(
    tickangle=-45
)

fig.update_traces(
    hovertemplate="<b>%{x}</b><br>Sales: ₹ %{y} Cr"
)
st.plotly_chart(
    fig,
    use_container_width=True
)


st.divider()

st.subheader("💰 Net Profit Trend")

fig = px.line(
    trend_data,
    x="year",
    y="net_profit",
    markers=True
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Net Profit (₹ Cr)",
    height=450,
    template="plotly_dark",
    hovermode="x unified"
)

fig.update_xaxes(
    tickangle=-45
)

fig.update_traces(
    hovertemplate="<b>%{x}</b><br>Net Profit: ₹ %{y} Cr"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.divider()

st.subheader("📊 Operating Profit Margin")

fig = px.line(
    trend_data,
    x="year",
    y="opm_percentage",
    markers=True
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="OPM (%)",
    height=450,
    template="plotly_dark",
    hovermode="x unified"
)

fig.update_xaxes(
    tickangle=-45
)

fig.update_traces(
    hovertemplate="<b>%{x}</b><br>OPM: %{y}%"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.divider()

st.subheader("📉 Return on Equity")

fig = px.line(
    roe_data,
    x="year",
    y="return_on_equity_pct",
    markers=True
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="ROE (%)",
    height=450,
    template="plotly_dark",
    hovermode="x unified"
)

fig.update_xaxes(
    tickangle=-45
)

fig.update_traces(
    hovertemplate="<b>%{x}</b><br>ROE: %{y}%"
)

st.plotly_chart(
    fig,
    use_container_width=True
)