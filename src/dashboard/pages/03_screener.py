import streamlit as st
import pandas as pd

from utils.db import get_screener_data

st.title("🔍 Stock Screener")

df = get_screener_data()

st.sidebar.header("Filters")

roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    50,
    15
)

de = st.sidebar.slider(
    "Maximum Debt / Equity",
    0.0,
    5.0,
    1.0
)

fcf = st.sidebar.slider(
    "Minimum Free Cash Flow",
    -5000,
    50000,
    0
)

filtered = df[
    (df["return_on_equity_pct"] >= roe)
    &
    (df["debt_to_equity"] <= de)
    &
    (df["free_cash_flow_cr"] >= fcf)
]

# -------------------------------
# Display Table
# -------------------------------

display_df = filtered.rename(columns={
    "company_name": "Company",
    "broad_sector": "Sector",
    "return_on_equity_pct": "ROE (%)",
    "debt_to_equity": "Debt / Equity",
    "free_cash_flow_cr": "Free Cash Flow (Cr)",
    "net_profit_margin_pct": "Net Profit Margin (%)",
    "operating_profit_margin_pct": "Operating Profit Margin (%)",
    "interest_coverage": "Interest Coverage"
})

# Hide unnecessary columns
display_df = display_df.drop(columns=["id", "year"])

st.success(f"📈 {len(display_df)} companies match your filters")

st.subheader("📊 Matching Companies")

st.dataframe(
    display_df.reset_index(drop=True),
    use_container_width=True
)

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download CSV",
    csv,
    "stock_screener.csv",
    "text/csv"
)