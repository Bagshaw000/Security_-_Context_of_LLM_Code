import datetime
import os

def generate_income_statement(revenue, expenses):
    net_income = revenue - expenses
    return f"Income Statement:\nRevenue: ${revenue:.2f}\nExpenses: ${expenses:.2f}\nNet Income: ${net_income:.2f}"

def generate_balance_sheet(assets, liabilities, equity):
    total_assets = assets
    total_liabilities = liabilities
    total_equity = equity
    return f"Balance Sheet:\nAssets: ${total_assets:.2f}\nLiabilities: ${total_liabilities:.2f}\nEquity: ${total_equity:.2f}"

def generate_cash_flow_statement(operating_cash_flow, investing_cash_flow, financing_cash_flow):
    total_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
    return f"Cash Flow Statement:\nOperating Cash Flow: ${operating_cash_flow:.2f}\nInvesting Cash Flow: ${investing_cash_flow:.2f}\nFinancing Cash Flow: ${financing_cash_flow:.2f}\nTotal Cash Flow: ${total_cash_flow:.2f}"

def generate_accounting_reports():
    revenue = 1000000
    expenses = 800000
    assets = 2000000
    liabilities = 1000000
    equity = 1000000
    operating_cash_flow = 150000
    investing_cash_flow = -50000
    financing_cash_flow = -100000

    income_statement = generate_income_statement(revenue, expenses)
    balance_sheet = generate_balance_sheet(assets, liabilities, equity)
    cash_flow_statement = generate_cash_flow_statement(operating_cash_flow, investing_cash_flow, financing_cash_flow)

    return income_statement, balance_sheet, cash_flow_statement

if __name__ == "__main__":
    income_statement, balance_sheet, cash_flow_statement = generate_accounting_reports()
    print(income_statement)
    print()
    print(balance_sheet)
    print()
    print(cash_flow_statement)