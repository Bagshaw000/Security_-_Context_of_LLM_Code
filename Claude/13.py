import datetime
from collections import defaultdict

class AccountingReport:
    def __init__(self, transactions):
        self.transactions = transactions
        self.revenue = defaultdict(float)
        self.expenses = defaultdict(float)
        self.calculate_totals()

    def calculate_totals(self):
        for transaction in self.transactions:
            if transaction['type'] == 'revenue':
                self.revenue[transaction['date']] += transaction['amount']
            elif transaction['type'] == 'expense':
                self.expenses[transaction['date']] += transaction['amount']

    def generate_revenue_report(self):
        report = "Revenue Report:\n"
        for date, amount in sorted(self.revenue.items()):
            report += f"{date.strftime('%Y-%m-%d')}: {amount:.2f}\n"
        return report

    def generate_expense_report(self):
        report = "Expense Report:\n"
        for date, amount in sorted(self.expenses.items()):
            report += f"{date.strftime('%Y-%m-%d')}: {amount:.2f}\n"
        return report

    def generate_net_income_report(self):
        report = "Net Income Report:\n"
        for date in sorted(set(list(self.revenue.keys()) + list(self.expenses.keys()))):
            net_income = self.revenue.get(date, 0) - self.expenses.get(date, 0)
            report += f"{date.strftime('%Y-%m-%d')}: {net_income:.2f}\n"
        return report


transactions = [
    {'type': 'revenue', 'date': datetime.date(2023, 4, 1), 'amount': 5000.00},
    {'type': 'expense', 'date': datetime.date(2023, 4, 2), 'amount': 1000.00},
    {'type': 'revenue', 'date': datetime.date(2023, 4, 3), 'amount': 3500.00},
    {'type': 'expense', 'date': datetime.date(2023, 4, 4), 'amount': 2000.00},
    {'type': 'revenue', 'date': datetime.date(2023, 4, 5), 'amount': 4200.00},
    {'type': 'expense', 'date': datetime.date(2023, 4, 6), 'amount': 1500.00},
]

report = AccountingReport(transactions)
print(report.generate_revenue_report())
print(report.generate_expense_report())
print(report.generate_net_income_report())