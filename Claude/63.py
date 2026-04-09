import pandas as pd
import datetime


data = pd.read_csv('accounting_data.csv')


total_revenue = data['revenue'].sum()
total_expenses = data['expenses'].sum()
net_profit = total_revenue - total_expenses


income_statement = pd.DataFrame({
    'Item': ['Revenue', 'Expenses', 'Net Profit'],
    'Amount': [total_revenue, total_expenses, net_profit]
})


assets = data['assets'].sum()
liabilities = data['liabilities'].sum()
equity = data['equity'].sum()

balance_sheet = pd.DataFrame({
    'Item': ['Assets', 'Liabilities', 'Equity'],
    'Amount': [assets, liabilities, equity]
})


cash_flow_statement = pd.DataFrame({
    'Item': ['Operating Activities', 'Investing Activities', 'Financing Activities'],
    'Amount': [data['cash_from_operations'].sum(), data['cash_from_investments'].sum(), data['cash_from_financing'].sum()]
})


income_statement.to_csv('income_statement.csv', index=False)
balance_sheet.to_csv('balance_sheet.csv', index=False)
cash_flow_statement.to_csv('cash_flow_statement.csv', index=False)