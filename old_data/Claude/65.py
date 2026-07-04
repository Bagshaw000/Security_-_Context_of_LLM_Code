import datetime
import pandas as pd

def generate_balance_sheet(assets, liabilities, equity):
    
    data = {
        'Assets': list(assets.keys()),
        'Amount': list(assets.values())
    }
    assets_df = pd.DataFrame(data)

    data = {
        'Liabilities': list(liabilities.keys()),
        'Amount': list(liabilities.values())
    }
    liabilities_df = pd.DataFrame(data)

    data = {
        'Equity': list(equity.keys()),
        'Amount': list(equity.values())
    }
    equity_df = pd.DataFrame(data)

    balance_sheet = pd.concat([assets_df, liabilities_df, equity_df])
    balance_sheet = balance_sheet.reset_index(drop=True)
    return balance_sheet

def generate_income_statement(revenue, expenses):
    
    data = {
        'Item': list(revenue.keys()) + list(expenses.keys()),
        'Amount': list(revenue.values()) + list(expenses.values())
    }
    income_statement = pd.DataFrame(data)
    income_statement['Type'] = ['Revenue'] * len(revenue) + ['Expense'] * len(expenses)
    return income_statement

def generate_cash_flow_statement(operating_activities, investing_activities, financing_activities):
    
    data = {
        'Activity': list(operating_activities.keys()) + list(investing_activities.keys()) + list(financing_activities.keys()),
        'Amount': list(operating_activities.values()) + list(investing_activities.values()) + list(financing_activities.values())
    }
    cash_flow_statement = pd.DataFrame(data)
    cash_flow_statement['Type'] = ['Operating'] * len(operating_activities) + ['Investing'] * len(investing_activities) + ['Financing'] * len(financing_activities)
    return cash_flow_statement

def generate_reports(assets, liabilities, equity, revenue, expenses, operating_activities, investing_activities, financing_activities):
    
    balance_sheet = generate_balance_sheet(assets, liabilities, equity)
    income_statement = generate_income_statement(revenue, expenses)
    cash_flow_statement = generate_cash_flow_statement(operating_activities, investing_activities, financing_activities)
    return balance_sheet, income_statement, cash_flow_statement


assets = {'Cash': 50000, 'Accounts Receivable': 20000, 'Inventory': 30000}
liabilities = {'Accounts Payable': 15000, 'Loans': 25000}
equity = {'Common Stock': 40000, 'Retained Earnings': 20000}
revenue = {'Sales': 100000}
expenses = {'Cost of Goods Sold': 60000, 'Salaries': 20000, 'Rent': 5000}
operating_activities = {'Net Income': 15000, 'Depreciation': 2000, 'Changes in Working Capital': -5000}
investing_activities = {'Purchase of Equipment': -10000, 'Sale of Investments': 5000}
financing_activities = {'Loan Repayment': -5000, 'Dividend Payout': -3000}

balance_sheet, income_statement, cash_flow_statement = generate_reports(assets, liabilities, equity, revenue, expenses, operating_activities, investing_activities, financing_activities)
print(balance_sheet)
print(income_statement)
print(cash_flow_statement)