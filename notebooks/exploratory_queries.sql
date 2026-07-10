-- =====================================================
-- Query 1: Total Companies
-- =====================================================
SELECT COUNT(*) AS total_companies
FROM companies;

-- =====================================================
-- Query 2: Top 10 Companies by ROE
-- =====================================================
SELECT
company_name,
roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- =====================================================
-- Query 3: Companies with Highest ROCE
-- =====================================================
SELECT
company_name,
roce_percentage
FROM companies
ORDER BY roce_percentage DESC
LIMIT 10;

-- =====================================================
-- Query 4: Average Sales by Year
-- =====================================================
SELECT
year,
ROUND(AVG(sales),2) AS average_sales
FROM profitandloss
GROUP BY year
ORDER BY year;

-- =====================================================
-- Query 5: Highest Net Profit
-- =====================================================
SELECT
company_id,
year,
net_profit
FROM profitandloss
ORDER BY net_profit DESC
LIMIT 10;

-- =====================================================
-- Query 6: Companies with Highest Borrowings
-- =====================================================
SELECT
company_id,
year,
borrowings
FROM balancesheet
ORDER BY borrowings DESC
LIMIT 10;

-- =====================================================
-- Query 7: Highest Operating Cash Flow
-- =====================================================
SELECT
company_id,
year,
operating_activity
FROM cashflow
ORDER BY operating_activity DESC
LIMIT 10;

-- =====================================================
-- Query 8: Companies Missing Annual Reports
-- =====================================================
SELECT
company_id,
Year
FROM documents
WHERE Annual_Report IS NULL;

-- =====================================================
-- Query 9: Total Records in Every Table
-- =====================================================
SELECT 'companies' AS table_name, COUNT(*) FROM companies
UNION ALL
SELECT 'profitandloss', COUNT(*) FROM profitandloss
UNION ALL
SELECT 'balancesheet', COUNT(*) FROM balancesheet
UNION ALL
SELECT 'cashflow', COUNT(*) FROM cashflow
UNION ALL
SELECT 'analysis', COUNT(*) FROM analysis
UNION ALL
SELECT 'documents', COUNT(*) FROM documents
UNION ALL
SELECT 'prosandcons', COUNT(*) FROM prosandcons
UNION ALL
SELECT 'financial_ratios', COUNT(*) FROM financial_ratios
UNION ALL
SELECT 'peer_groups', COUNT(*) FROM peer_groups
UNION ALL
SELECT 'stock_prices', COUNT(*) FROM stock_prices
UNION ALL
SELECT 'sectors', COUNT(*) FROM sectors;

-- =====================================================
-- Query 10: Company Financial Overview
-- =====================================================
SELECT
c.company_name,
p.year,
p.sales,
p.net_profit,
b.total_assets,
cf.net_cash_flow
FROM companies c
JOIN profitandloss p
ON c.id = p.company_id
JOIN balancesheet b
ON p.company_id = b.company_id
AND p.year = b.year
JOIN cashflow cf
ON p.company_id = cf.company_id
AND p.year = cf.year
LIMIT 20;