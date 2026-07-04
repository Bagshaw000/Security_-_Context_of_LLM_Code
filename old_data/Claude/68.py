import datetime
import pandas as pd

def generate_income_statement(revenue, expenses):
    net_income = revenue - expenses
    income_statement = pd.DataFrame({
        'Account': ['Revenue', 'Expenses', 'Net Income'],
        'Amount': [revenue, expenses, net_income]
    })
    return income_statement

def generate_balance_sheet(assets, liabilities, equity):
    total_assets = sum(assets.values())
    total_liabilities = sum(liabilities.values())
    total_equity = sum(equity.values())
    balance_sheet = pd.DataFrame({
        'Account': ['Assets', 'Liabilities', 'Equity'],
        'Amount': [total_assets, total_liabilities, total_equity]
    })
    return balance_sheet

def generate_cash_flow_statement(beginning_cash, operating_cash_flow, investing_cash_flow, financing_cash_flow):
    ending_cash = beginning_cash + operating_cash_flow + investing_cash_flow + financing_cash_flow
    cash_flow_statement = pd.DataFrame({
        'Account': ['Beginning Cash', 'Operating Cash Flow', 'Investing Cash Flow', 'Financing Cash Flow', 'Ending Cash'],
        'Amount': [beginning_cash, operating_cash_flow, investing_cash_flow, financing_cash_flow, ending_cash]
    })
    return cash_flow_statement


revenue = 1000000
expenses = 800000
assets = {'Cash': 100000, 'Accounts Receivable': 200000, 'Inventory': 300000}
liabilities = {'Accounts Payable': 150000, 'Loans': 250000}
equity = {'Common Stock': 100000, 'Retained Earnings': 100000}
beginning_cash = 50000
operating_cash_flow = 75000
investing_cash_flow = -50000
financing_cash_flow = 25000

income_statement = generate_income_statement(revenue, expenses)
print(income_statement)

balance_sheet = generate_balance_sheet(assets, liabilities, equity)
print(balance_sheet)

cash_flow_statement = generate_cash_flow_statement(beginning_cash, operating_cash_flow, investing_cash_flow, financing_cash_flow)
print(cash_flow_statement)