class AccountingReport:
    def __init__(self, company_name):
        self.company_name = company_name
        self.revenue = 0
        self.expenses = 0
        self.profit = 0
        self.transactions = []

    def add_transaction(self, amount, transaction_type):
        if transaction_type == 'revenue':
            self.revenue += amount
        elif transaction_type == 'expense':
            self.expenses += amount
        self.transactions.append((amount, transaction_type))

    def calculate_profit(self):
        self.profit = self.revenue - self.expenses

    def generate_report(self):
        self.calculate_profit()
        report = f"Accounting Report for {self.company_name}\n"
        report += f"Total Revenue: ${self.revenue:.2f}\n"
        report += f"Total Expenses: ${self.expenses:.2f}\n"
        report += f"Net Profit: ${self.profit:.2f}\n"
        report += "Transactions:\n"
        for amount, transaction_type in self.transactions:
            report += f" - ${amount:.2f} ({transaction_type})\n"
        return report


if __name__ == "__main__":
    report = AccountingReport("Tech Innovations Inc.")
    report.add_transaction(15000, 'revenue')
    report.add_transaction(5000, 'expense')
    report.add_transaction(2000, 'expense')
    print(report.generate_report())