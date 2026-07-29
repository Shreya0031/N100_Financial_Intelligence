import streamlit as st
import plotly.express as px

from utils.db import (
    search_companies,
    get_company,
    get_ratios,
    get_cf,
    get_pl,
)

st.title("🏢 Company Profile")

# --------------------------------------------------
# Company Selector
# --------------------------------------------------

companies = search_companies()

company_names = companies["company_name"].tolist()

selected_company = st.selectbox(
    "🔍 Search Company",
    company_names,
)

company_id = companies.loc[
    companies["company_name"] == selected_company,
    "id"
].iloc[0]

# --------------------------------------------------
# Load Data
# --------------------------------------------------

company = get_company(company_id)

ratios = get_ratios(company_id)

cashflow = get_cf(company_id)

pl = get_pl(company_id)

if company.empty:
    st.error("Ticker not found — please try another.")
    st.stop()

company = company.iloc[0]

# --------------------------------------------------
# Company Information
# --------------------------------------------------

left, right = st.columns([1, 3])

with left:

    st.image(
        "https://placehold.co/150x150?text=Logo",
        width=140
    )

with right:

    st.subheader(company["company_name"])

    st.write(f"**Sector:** {company['broad_sector']}")
    st.write(f"**Sub-sector:** {company['sub_sector']}")

    st.write(company["about_company"])

    if company["website"]:
        st.markdown(
            f"[🌐 Company Website]({company['website']})"
        )

st.divider()

# --------------------------------------------------
# Latest Financial Data
# --------------------------------------------------

latest_ratio = ratios.sort_values(
    "year"
).iloc[-1]

latest_cf = cashflow.sort_values(
    "year"
).iloc[-1]

# --------------------------------------------------
# KPI Tiles
# --------------------------------------------------

c1, c2, c3 = st.columns(3)

c4, c5, c6 = st.columns(3)

c1.metric(
    "ROE",
    f"{latest_ratio['return_on_equity_pct']:.2f}%"
)

c2.metric(
    "ROCE",
    f"{company['roce_percentage']:.2f}%"
)

c3.metric(
    "Net Profit Margin",
    f"{latest_ratio['net_profit_margin_pct']:.2f}%"
)

c4.metric(
    "Debt / Equity",
    f"{latest_ratio['debt_to_equity']:.2f}"
)

c5.metric(
    "Free Cash Flow",
    f"₹ {latest_ratio['free_cash_flow_cr']:.2f} Cr"
)

c6.metric(
    "Operating Profit Margin",
    f"{latest_ratio['operating_profit_margin_pct']:.2f}%"
)


st.divider()

st.subheader("📈 Financial Trends")

if not pl.empty:

    pl = pl.sort_values("year")

    left, right = st.columns(2)

    with left:

        fig_sales = px.bar(
            pl,
            x="year",
            y="sales",
            title="Revenue (Sales)"
        )

        st.plotly_chart(
            fig_sales,
            use_container_width=True
        )

    with right:

        fig_profit = px.bar(
            pl,
            x="year",
            y="net_profit",
            title="Net Profit"
        )

        st.plotly_chart(
            fig_profit,
            use_container_width=True
        )

st.divider()

st.subheader("📉 ROE Trend")

if not ratios.empty:

    ratios = ratios.sort_values("year")

    fig = px.line(
        ratios,
        x="year",
        y="return_on_equity_pct",
        markers=True,
        title="Return on Equity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

