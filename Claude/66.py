import datetime
import pandas as pd

def generate_income_statement(revenues, expenses):
    income = sum(revenues) - sum(expenses)
    return pd.DataFrame({
        'Account': ['Revenues', 'Expenses', 'Net Income'],
        'Amount': [sum(revenues), sum(expenses), income]
    })

def generate_balance_sheet(assets, liabilities, equity):
    total_assets = sum(assets)
    total_liabilities = sum(liabilities)
    total_equity = sum(equity)
    return pd.DataFrame({
        'Account': ['Assets', 'Liabilities', 'Equity'],
        'Amount': [total_assets, total_liabilities, total_equity]
    })

def generate_cash_flow_statement(operating_cash_flows, investing_cash_flows, financing_cash_flows):
    net_cash_flow = sum(operating_cash_flows) + sum(investing_cash_flows) + sum(financing_cash_flows)
    return pd.DataFrame({
        'Account': ['Operating Cash Flows', 'Investing Cash Flows', 'Financing Cash Flows', 'Net Cash Flow'],
        'Amount': [sum(operating_cash_flows), sum(investing_cash_flows), sum(financing_cash_flows), net_cash_flow]
    })


revenues = [100000, 120000, 150000]
expenses = [80000, 90000, 100000]
assets = [500000, 550000, 600000]
liabilities = [300000, 320000, 350000]
equity = [200000, 230000, 250000]
operating_cash_flows = [50000, 60000, 70000]
investing_cash_flows = [-20000, -30000, -40000]
financing_cash_flows = [10000, 20000, 30000]

income_statement = generate_income_statement(revenues, expenses)
balance_sheet = generate_balance_sheet(assets, liabilities, equity)
cash_flow_statement = generate_cash_flow_statement(operating_cash_flows, investing_cash_flows, financing_cash_flows)

print(income_statement)
print(balance_sheet)
print(cash_flow_statement)