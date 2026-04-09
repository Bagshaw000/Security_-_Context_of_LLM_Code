import datetime
import pandas as pd

def generate_income_statement(revenue, expenses):
    net_income = revenue - expenses
    income_statement = pd.DataFrame({
        'Item': ['Revenue', 'Expenses', 'Net Income'],
        'Amount': [revenue, expenses, net_income]
    })
    return income_statement

def generate_balance_sheet(assets, liabilities, equity):
    total_assets = assets
    total_liabilities = liabilities
    total_equity = equity
    balance_sheet = pd.DataFrame({
        'Item': ['Assets', 'Liabilities', 'Equity'],
        'Amount': [total_assets, total_liabilities, total_equity]
    })
    return balance_sheet

def generate_cash_flow_statement(operating_cash_flow, investing_cash_flow, financing_cash_flow):
    total_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
    cash_flow_statement = pd.DataFrame({
        'Item': ['Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'Total Cash Flow'],
        'Amount': [operating_cash_flow, investing_cash_flow, financing_cash_flow, total_cash_flow]
    })
    return cash_flow_statement


revenue = 1000000
expenses = 800000
assets = 2000000
liabilities = 1500000
equity = 500000
operating_cash_flow = 200000
investing_cash_flow = -50000
financing_cash_flow = -100000

income_statement = generate_income_statement(revenue, expenses)
print(income_statement)

balance_sheet = generate_balance_sheet(assets, liabilities, equity)
print(balance_sheet)

cash_flow_statement = generate_cash_flow_statement(operating_cash_flow, investing_cash_flow, financing_cash_flow)
print(cash_flow_statement)