PRAGMA foreign_keys = ON;

----------------------------------------------------
-- Companies
----------------------------------------------------

CREATE TABLE IF NOT EXISTS companies (
    id TEXT PRIMARY KEY,
    company_logo TEXT,
    company_name TEXT,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);

----------------------------------------------------
-- Profit & Loss
----------------------------------------------------

CREATE TABLE IF NOT EXISTS profitandloss (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    sales REAL,

    expenses REAL,

    operating_profit REAL,

    opm_percentage REAL,

    other_income REAL,

    interest REAL,

    depreciation REAL,

    profit_before_tax REAL,

    tax_percentage REAL,

    net_profit REAL,

    eps REAL,

    dividend_payout REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

----------------------------------------------------
-- Balance Sheet
----------------------------------------------------

CREATE TABLE IF NOT EXISTS balancesheet (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    equity_capital REAL,

    reserves REAL,

    borrowings REAL,

    other_liabilities REAL,

    total_liabilities REAL,

    fixed_assets REAL,

    cwip REAL,

    investments REAL,

    other_asset REAL,

    total_assets REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

----------------------------------------------------
-- Cash Flow
----------------------------------------------------

CREATE TABLE IF NOT EXISTS cashflow (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    operating_activity REAL,

    investing_activity REAL,

    financing_activity REAL,

    net_cash_flow REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

----------------------------------------------------
-- Analysis
----------------------------------------------------

CREATE TABLE IF NOT EXISTS analysis (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year INTEGER,

    metric TEXT,

    value REAL,

    remarks TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

----------------------------------------------------
-- Documents
----------------------------------------------------

CREATE TABLE IF NOT EXISTS documents (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    Year INTEGER,

    Annual_Report TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

----------------------------------------------------
-- Pros & Cons
----------------------------------------------------

CREATE TABLE IF NOT EXISTS prosandcons (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    pros TEXT,

    cons TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

----------------------------------------------------
-- Sectors
----------------------------------------------------

CREATE TABLE IF NOT EXISTS sectors (

    id INTEGER PRIMARY KEY,

    sector_name TEXT,

    company_count INTEGER,

    avg_roe REAL,

    avg_roce REAL,

    market_cap REAL
);

----------------------------------------------------
-- Stock Prices
----------------------------------------------------

CREATE TABLE IF NOT EXISTS stock_prices (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    trading_date TEXT,

    open_price REAL,

    high_price REAL,

    low_price REAL,

    close_price REAL,

    volume INTEGER,

    market_cap REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

----------------------------------------------------
-- Financial Ratios
----------------------------------------------------

CREATE TABLE IF NOT EXISTS financial_ratios (

    id INTEGER PRIMARY KEY,

    company_id TEXT,

    year TEXT,

    pe_ratio REAL,

    pb_ratio REAL,

    roce REAL,

    debt_to_equity REAL,

    current_ratio REAL,

    roe REAL,

    eps REAL,

    dividend_yield REAL,

    book_value REAL,

    face_value REAL,

    total_debt_cr REAL,

    cash_from_operations_cr REAL
);