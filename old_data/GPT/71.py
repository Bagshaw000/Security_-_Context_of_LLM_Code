import pandas as pd

class AccountingReport:
    def __init__(self, transactions):
        self.transactions = transactions

    def generate_report(self):
        df = pd.DataFrame(self.transactions)
        report = {
            'Total Revenue': df[df['Type'] == 'Revenue']['Amount'].sum(),
            'Total Expenses': df[df['Type'] == 'Expense']['Amount'].sum(),
            'Net Income': df[df['Type'] == 'Revenue']['Amount'].sum() - df[df['Type'] == 'Expense']['Amount'].sum()
        }
        return report


transactions = [
    {'Type': 'Revenue', 'Amount': 1000},
    {'Type': 'Expense', 'Amount': 300},
    {'Type': 'Revenue', 'Amount': 500},
    {'Type': 'Expense', 'Amount': 200},
]

report_generator = AccountingReport(transactions)
report = report_generator.generate_report()
print(report)