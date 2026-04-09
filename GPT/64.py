import pandas as pd

class AccountingReport:
    def __init__(self, transactions):
        self.transactions = transactions

    def generate_report(self):
        df = pd.DataFrame(self.transactions)
        report = {
            'Total Income': df[df['Type'] == 'Income']['Amount'].sum(),
            'Total Expenses': df[df['Type'] == 'Expense']['Amount'].sum(),
            'Net Profit': df[df['Type'] == 'Income']['Amount'].sum() - df[df['Type'] == 'Expense']['Amount'].sum(),
            'Income Breakdown': df[df['Type'] == 'Income'].groupby('Category')['Amount'].sum(),
            'Expense Breakdown': df[df['Type'] == 'Expense'].groupby('Category')['Amount'].sum(),
        }
        return report


transactions = [
    {'Type': 'Income', 'Amount': 1000, 'Category': 'Sales'},
    {'Type': 'Income', 'Amount': 500, 'Category': 'Services'},
    {'Type': 'Expense', 'Amount': 300, 'Category': 'Rent'},
    {'Type': 'Expense', 'Amount': 200, 'Category': 'Utilities'},
]

report_generator = AccountingReport(transactions)
report = report_generator.generate_report()
print(report)