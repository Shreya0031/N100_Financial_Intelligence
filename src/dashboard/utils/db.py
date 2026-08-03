import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# --------------------------------------------------
# Database Path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = PROJECT_ROOT / "db" / "nifty100.db"


# --------------------------------------------------
# Connection
# --------------------------------------------------

@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# --------------------------------------------------
# Generic Query
# --------------------------------------------------

@st.cache_data(ttl=600)
def run_query(query, params=()):
    conn = get_connection()
    return pd.read_sql_query(query, conn, params=params)


# --------------------------------------------------
# Company Search
# --------------------------------------------------

@st.cache_data(ttl=600)
def search_companies():
    return run_query("""
        SELECT
            id,
            company_name
        FROM companies
        ORDER BY company_name
    """)


# --------------------------------------------------
# Company Details
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_company(company_id):
    return run_query("""
        SELECT
            c.id,
            c.company_name,
            c.company_logo,
            c.about_company,
            c.website,
            c.face_value,
            c.book_value,
            c.roe_percentage,
            c.roce_percentage,
            s.broad_sector,
            s.sub_sector,
            s.market_cap_category,
            s.index_weight_pct
        FROM companies c
        LEFT JOIN sectors s
            ON c.id = s.company_id
        WHERE c.id = ?
    """, (company_id,))


# --------------------------------------------------
# All Companies
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_companies():
    return run_query("""
        SELECT
            c.id,
            c.company_name,
            c.company_logo,
            c.about_company,
            c.website,
            c.face_value,
            c.book_value,
            c.roe_percentage,
            c.roce_percentage,
            s.broad_sector,
            s.sub_sector,
            s.market_cap_category,
            s.index_weight_pct
        FROM companies c
        LEFT JOIN sectors s
            ON c.id = s.company_id
        ORDER BY c.company_name
    """)


# --------------------------------------------------
# Financial Ratios
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_ratios(company_id, year=None):

    if year is None:
        return run_query("""
            SELECT *
            FROM financial_ratios
            WHERE company_id = ?
            ORDER BY year
        """, (company_id,))

    return run_query("""
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
          AND year = ?
    """, (company_id, year))


# --------------------------------------------------
# Profit & Loss
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_pl(company_id):
    return run_query("""
        SELECT *
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY year
    """, (company_id,))


# --------------------------------------------------
# Balance Sheet
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_bs(company_id):
    return run_query("""
        SELECT *
        FROM balancesheet
        WHERE company_id = ?
        ORDER BY year
    """, (company_id,))


# --------------------------------------------------
# Cash Flow
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_cf(company_id):
    return run_query("""
        SELECT *
        FROM cashflow
        WHERE company_id = ?
        ORDER BY year
    """, (company_id,))


# --------------------------------------------------
# Sectors
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_sectors():
    return run_query("""
        SELECT *
        FROM sectors
        ORDER BY broad_sector
    """)


# --------------------------------------------------
# Peer Groups
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_peers(group_name):
    return run_query("""
        SELECT *
        FROM peer_groups
        WHERE broad_sector = ?
    """, (group_name,))


# --------------------------------------------------
# Pros & Cons
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_pros_cons(company_id):
    return run_query("""
        SELECT
            pros,
            cons
        FROM prosandcons
        WHERE company_id = ?
    """, (company_id,))


# --------------------------------------------------
# Screener Data
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_screener_data():

    return run_query("""
        SELECT
            c.id,
            c.company_name,
            s.broad_sector,

            fr.year,
            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.free_cash_flow_cr,
            fr.net_profit_margin_pct,
            fr.operating_profit_margin_pct,
            fr.interest_coverage

        FROM financial_ratios fr

        JOIN companies c
            ON c.id = fr.company_id

        LEFT JOIN sectors s
            ON c.id = s.company_id

        WHERE fr.year = (
            SELECT MAX(year)
            FROM financial_ratios
        )

        ORDER BY c.company_name
    """)


# --------------------------------------------------
# Peer Group Names
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_peer_group_names():
    return run_query("""
        SELECT DISTINCT peer_group_name
        FROM peer_groups
        ORDER BY peer_group_name
    """)


# --------------------------------------------------
# Companies in Peer Group
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_peer_companies(group_name):
    return run_query("""
        SELECT
            pg.company_id,
            c.company_name,
            pg.is_benchmark
        FROM peer_groups pg
        JOIN companies c
            ON pg.company_id = c.id
        WHERE pg.peer_group_name = ?
        ORDER BY c.company_name
    """, (group_name,))


# --------------------------------------------------
# Peer Percentiles
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_peer_percentiles(company_id):
    return run_query("""
        SELECT
            metric,
            percentile_rank
        FROM peer_percentiles
        WHERE company_id = ?
        ORDER BY metric
    """, (company_id,))

# --------------------------------------------------
# Peer Average Percentiles
# --------------------------------------------------

@st.cache_data(ttl=600)
def get_peer_average_percentiles(group_name):
    return run_query("""
        SELECT
            metric,
            AVG(percentile_rank) AS percentile_rank
        FROM peer_percentiles
        WHERE peer_group_name = ?
        GROUP BY metric
        ORDER BY metric
    """, (group_name,))



@st.cache_data(ttl=600)
def get_company_list():
    return run_query("""
        SELECT
            id,
            company_name
        FROM companies
        ORDER BY company_name
    """)

@st.cache_data(ttl=600)
def get_trend_data(company_id):
    return run_query("""
        SELECT
            year,
            sales,
            net_profit,
            opm_percentage
        FROM profitandloss
        WHERE company_id = ?
        ORDER BY year
    """, (company_id,))


@st.cache_data(ttl=600)
def get_roe_trend(company_id):
    return run_query("""
        SELECT
            year,
            return_on_equity_pct
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year
    """, (company_id,))



@st.cache_data
def show_company_columns():
    return run_query("""
        PRAGMA table_info(companies)
    """)

@st.cache_data
def show_tables():
    return run_query("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """)

@st.cache_data
def show_analysis_columns():
    return run_query("""
        PRAGMA table_info(analysis)
    """)

@st.cache_data
def show_table_columns(table_name):
    return run_query(f"""
        PRAGMA table_info({table_name})
    """)

@st.cache_data(ttl=600)
def get_metric_comparison(metric):

    query = f"""
    SELECT
        c.company_name,
        fr.year,
        MAX(fr.{metric}) AS {metric}

    FROM financial_ratios fr

    JOIN companies c
        ON c.id = fr.company_id

    WHERE fr.year = (
        SELECT MAX(fr2.year)
        FROM financial_ratios fr2
        WHERE fr2.company_id = fr.company_id
    )

    GROUP BY
        c.company_name,
        fr.year

    ORDER BY
        {metric} DESC
    """

    return run_query(query)


@st.cache_data(ttl=600)
def debug_metric():
    return run_query("""
        SELECT *
        FROM financial_ratios
        LIMIT 20
    """)


@st.cache_data
def show_financial_ratio_columns():
    return run_query("""
        PRAGMA table_info(financial_ratios)
    """)


@st.cache_data(ttl=600)
def get_capital_metrics():
    return run_query("""
        SELECT DISTINCT
            c.company_name,
            fr.year,
            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.free_cash_flow_cr,
            fr.asset_turnover,
            fr.interest_coverage
        FROM financial_ratios fr
        JOIN companies c
            ON fr.company_id = c.id
        WHERE fr.year = (
            SELECT MAX(fr2.year)
            FROM financial_ratios fr2
            WHERE fr2.company_id = fr.company_id
        )
        ORDER BY c.company_name
    """)

@st.cache_data(ttl=600)
def get_report_data():
    return run_query("""
        SELECT
            c.company_name,
            fr.year,
            fr.return_on_equity_pct,
            fr.debt_to_equity,
            fr.free_cash_flow_cr
        FROM financial_ratios fr
        JOIN companies c
            ON fr.company_id = c.id
        WHERE fr.year = (
            SELECT MAX(fr2.year)
            FROM financial_ratios fr2
            WHERE fr2.company_id = fr.company_id
        )
        ORDER BY c.company_name
    """)