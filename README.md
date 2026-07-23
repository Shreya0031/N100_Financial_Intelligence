# 📊 N100 Financial Intelligence Platform

A Python-based **Financial Intelligence Platform** built to analyze **NIFTY 100** companies using financial statements. The platform automates data ingestion, computes financial KPIs, performs peer benchmarking, generates radar chart visualizations, and creates professional Excel reports for financial analysis.

---

## 🚀 Features

- ✅ Automated ETL Pipeline
- ✅ SQLite Database Integration
- ✅ Financial Ratio Analysis
- ✅ CAGR (Compound Annual Growth Rate) Analysis
- ✅ Cash Flow KPI Analysis
- ✅ Peer Group Benchmarking
- ✅ Percentile Ranking Engine
- ✅ Benchmark Company Identification
- ✅ Radar Charts with Peer Average Overlay
- ✅ Professional Excel Peer Comparison Reports
- ✅ Median Summary Analytics
- ✅ Automated Testing with Pytest

---

## 📂 Project Structure

```text
N100_Financial_Intelligence/
│
├── data/
│   ├── analysis.xlsx
│   ├── balancesheet.xlsx
│   ├── cashflow.xlsx
│   ├── companies.xlsx
│   ├── financial_ratios.xlsx
│   ├── market_cap.xlsx
│   ├── peer_groups.xlsx
│   ├── profitandloss.xlsx
│   ├── sectors.xlsx
│   └── stock_prices.xlsx
│
├── db/
│   ├── nifty100.db
│   └── schema.sql
│
├── reports/
│   ├── radar_charts/
│   └── peer_comparison.xlsx
│
├── src/
│   ├── analytics/
│   │   ├── ratios.py
│   │   ├── cagr.py
│   │   ├── cashflow_kpis.py
│   │   └── peer.py
│   │
│   ├── etl/
│   │
│   ├── reporting/
│   │   └── peer_report.py
│   │
│   ├── screener/
│   │
│   └── visualization/
│       └── radar.py
│
├── tests/
├── requirements.txt
├── Makefile
└── README.md
```

---

# 🛠 Technologies Used

- Python 3.13
- Pandas
- NumPy
- Matplotlib
- SQLite3
- OpenPyXL
- Pytest

---

# 📊 Financial Analytics

The platform automatically computes:

- Return on Equity (ROE)
- Net Profit Margin
- Asset Turnover Ratio
- Debt-to-Equity Ratio
- Interest Coverage Ratio
- Free Cash Flow
- Sales CAGR
- Profit CAGR
- Peer Percentile Rankings

---

# 📈 Visualizations

## Radar Charts

A radar chart is generated for every company showing:

- Financial KPI comparison
- Peer Average Overlay
- Visual benchmarking

Generated inside:

```text
reports/radar_charts/
```

---

# 📑 Excel Peer Comparison Report

Generated automatically at:

```text
reports/peer_comparison.xlsx
```

### Features

- Separate worksheet for every peer group
- Professional formatting
- Conditional formatting
- Auto-sized columns
- Frozen header row
- Benchmark company highlighted
- Median summary row
- Percentile ranking comparison

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/Shreya0031/N100_Financial_Intelligence
```

Move into the project

```bash
cd N100_Financial_Intelligence
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Project

## 1. Create Database

```bash
python src/etl/create_database.py
```

---

## 2. Calculate Financial Ratios

```bash
python src/analytics/ratios.py
```

---

## 3. Calculate CAGR

```bash
python src/analytics/cagr.py
```

---

## 4. Calculate Cash Flow KPIs

```bash
python src/analytics/cashflow_kpis.py
```

---

## 5. Generate Peer Percentile Rankings

```bash
python src/analytics/peer.py
```

---

## 6. Generate Radar Charts

```bash
python src/visualization/radar.py
```

---

## 7. Generate Peer Comparison Excel Report

```bash
python src/reporting/peer_report.py
```

---

# ✅ Running Tests

Execute all automated tests:

```bash
python -m pytest
```

Expected output:

```text
55 passed
```

---

# 📊 Output

After execution, the project generates:

```text
reports/
│
├── radar_charts/
│     ├── TCS.png
│     ├── INFY.png
│     ├── RELIANCE.png
│     └── ...
│
└── peer_comparison.xlsx
```

---

# 📌 Project Modules

## ETL Module

- Imports Excel datasets
- Cleans financial data
- Loads SQLite database

---

## Analytics Module

Computes:

- Financial Ratios
- CAGR
- Cash Flow KPIs
- Peer Percentiles

---

## Visualization Module

Creates:

- Radar Charts
- Peer Average Comparison

---

## Reporting Module

Creates professional Excel reports with:

- Peer Group Worksheets
- Benchmark Highlighting
- Median Summary
- Conditional Formatting

---

# 🚀 Future Improvements

- Interactive Streamlit Dashboard
- Company Search
- KPI Cards
- Historical Trend Analysis
- Interactive Financial Charts
- PDF Report Export
- Dashboard Deployment
- REST API Integration

---

# 📌 Project Highlights

- Financial Intelligence Platform
- Automated ETL Pipeline
- SQLite Database
- Financial KPI Engine
- CAGR Analysis
- Cash Flow Analytics
- Peer Benchmarking
- Percentile Ranking Engine
- Radar Chart Visualization
- Professional Excel Reporting
- Benchmark Company Highlighting
- Median Summary Analytics
- Modular Python Architecture
- Automated Testing
- 55+ Passing Tests

---

# 👩‍💻 Author

**Shreya Singh**

B.Tech Computer Science & Engineering

Financial Intelligence Platform

---
