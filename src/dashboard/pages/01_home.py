import streamlit as st
import plotly.express as px

from utils.db import get_companies, run_query

st.title("🏠 Nifty 100 Dashboard")

# -------------------------------
# Sidebar
# -------------------------------

years = run_query("""
    SELECT DISTINCT year
    FROM financial_ratios
    ORDER BY year
""")

selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    years["year"].tolist()
)

# -------------------------------
# KPI Queries
# -------------------------------

kpi = run_query("""
SELECT
    ROUND(AVG(return_on_equity_pct),2) AS avg_roe,
    ROUND(AVG(debt_to_equity),2) AS avg_de,
    COUNT(DISTINCT company_id) AS total_companies,
    SUM(CASE WHEN debt_to_equity=0 THEN 1 ELSE 0 END) AS debt_free
FROM financial_ratios
WHERE year = ?
""", (selected_year,))

# -------------------------------
# KPI Cards
# -------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average ROE", f"{kpi.iloc[0]['avg_roe']} %")
col2.metric("Average D/E", kpi.iloc[0]["avg_de"])
col3.metric("Companies", int(kpi.iloc[0]["total_companies"]))
col4.metric("Debt Free", int(kpi.iloc[0]["debt_free"]))

st.divider()

# -------------------------------
# Sector Distribution
# -------------------------------

sector = run_query("""
SELECT
    broad_sector,
    COUNT(*) as companies
FROM sectors
GROUP BY broad_sector
ORDER BY companies DESC
""")

fig = px.pie(
    sector,
    names="broad_sector",
    values="companies",
    hole=0.45,
    title="Sector Distribution"
)

st.plotly_chart(fig, use_container_width=True)