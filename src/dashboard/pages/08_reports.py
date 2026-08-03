import streamlit as st
from utils.db import get_report_data

st.title("📄 Annual Reports")

# Load data
df = get_report_data()

df = df.sort_values(
    by="return_on_equity_pct",
    ascending=False
)

display_df = df.rename(columns={
    "company_name": "Company",
    "year": "Year",
    "return_on_equity_pct": "ROE (%)",
    "debt_to_equity": "Debt/Equity",
    "free_cash_flow_cr": "Free Cash Flow (Cr)"
})

col1, col2, col3 = st.columns(3)

col1.metric(
    "Companies",
    df["company_name"].nunique()
)

col2.metric(
    "Latest Year",
    df["year"].iloc[0]
)

col3.metric(
    "Average ROE",
    f"{df['return_on_equity_pct'].mean():.2f}%"
)

st.divider()

# Show table
st.subheader("Latest Financial Report")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# Download button
st.download_button(
    label="📥 Download CSV Report",
    data=display_df.to_csv(index=False),
    file_name="annual_report.csv",
    mime="text/csv"
)