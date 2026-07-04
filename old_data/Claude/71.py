import pandas as pd


data = pd.read_csv('accounting_data.csv')


total_revenue = data['revenue'].sum()


total_expenses = data['expenses'].sum()


net_profit = total_revenue - total_expenses


monthly_data = data.groupby(pd.to_datetime(data['date']).dt.strftime('%Y-%m')).sum()


income_statement = pd.DataFrame({
    'Month': monthly_data.index,
    'Revenue': monthly_data['revenue'],
    'Expenses': monthly_data['expenses'],
    'Net Profit': monthly_data['revenue'] - monthly_data['expenses']
})


balance_sheet = pd.DataFrame({
    'Assets': [data['assets'].sum()],
    'Liabilities': [data['liabilities'].sum()],
    'Equity': [data['equity'].sum()]
}, index=['Total'])


print('Income Statement:')
print(income_statement)
print('\nBalance Sheet:')
print(balance_sheet)