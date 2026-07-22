import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.analytics.ratios import *
from src.analytics.cagr import *
from src.analytics.cashflow_kpis import *

print("Testing Ratios...")
print(net_profit_margin(200, 1000))
print(return_on_equity(200, 500, 500))
print(asset_turnover(1000, 500))

print("\nTesting CAGR...")
print(calculate_cagr(100, 200, 5))

print("\nTesting Cash Flow...")
print(free_cash_flow(500, -200))
print(cfo_quality_score(300, 200))