import pandas as pd


data = {
    'Date': ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15'],
    'Description': ['Income', 'Expense', 'Income', 'Expense'],
    'Amount': [1000, -200, 1500, -300]
}


df = pd.DataFrame(data)


total_income = df[df['Amount'] > 0]['Amount'].sum()
total_expenses = df[df['Amount'] < 0]['Amount'].sum()


report = {
    'Total Income': total_income,
    'Total Expenses': total_expenses,
    'Net Profit/Loss': total_income + total_expenses
}


report_df = pd.DataFrame(list(report.items()), columns=['Description', 'Amount'])


report_df.to_excel('accounting_report.xlsx', index=False)