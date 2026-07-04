import pandas as pd

class AccountingReport:
    def __init__(self, transactions):
        self.transactions = transactions

    def generate_report(self):
        df = pd.DataFrame(self.transactions)
        report = {
            'Total Income': df[df['Type'] == 'Income']['Amount'].sum(),
            'Total Expenses': df[df['Type'] == 'Expense']['Amount'].sum(),
            'Net Profit/Loss': df[df['Type'] == 'Income']['Amount'].sum() - df[df['Type'] == 'Expense']['Amount'].sum(),
            'Income Breakdown': df[df['Type'] == 'Income'].groupby('Category')['Amount'].sum(),
            'Expense Breakdown': df[df['Type'] == 'Expense'].groupby('Category')['Amount'].sum()
        }
        return report


transactions = [
    {'Type': 'Income', 'Category': 'Sales', 'Amount': 1000},
    {'Type': 'Income', 'Category': 'Investment', 'Amount': 500},
    {'Type': 'Expense', 'Category': 'Rent', 'Amount': 300},
    {'Type': 'Expense', 'Category': 'Utilities', 'Amount': 200},
]

report_generator = AccountingReport(transactions)
report = report_generator.generate_report()
print(report)