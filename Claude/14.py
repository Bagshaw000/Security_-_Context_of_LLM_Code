import datetime
import os

def generate_income_statement(revenue, expenses):
    net_income = revenue - expenses
    print("Income Statement:")
    print("Revenue: $", revenue)
    print("Expenses: $", expenses)
    print("Net Income: $", net_income)

def generate_balance_sheet(assets, liabilities, equity):
    total_assets = assets
    total_liabilities = liabilities
    total_equity = equity
    print("Balance Sheet:")
    print("Assets: $", total_assets)
    print("Liabilities: $", total_liabilities)
    print("Equity: $", total_equity)

def generate_cash_flow_statement(cash_from_operations, cash_from_investing, cash_from_financing):
    net_cash_flow = cash_from_operations + cash_from_investing + cash_from_financing
    print("Cash Flow Statement:")
    print("Cash from Operations: $", cash_from_operations)
    print("Cash from Investing: $", cash_from_investing)
    print("Cash from Financing: $", cash_from_financing)
    print("Net Cash Flow: $", net_cash_flow)

def main():
    revenue = 100000
    expenses = 80000
    assets = 200000
    liabilities = 100000
    equity = 100000
    cash_from_operations = 50000
    cash_from_investing = -20000
    cash_from_financing = 10000

    generate_income_statement(revenue, expenses)
    print()
    generate_balance_sheet(assets, liabilities, equity)
    print()
    generate_cash_flow_statement(cash_from_operations, cash_from_investing, cash_from_financing)

if __name__ == "__main__":
    main()