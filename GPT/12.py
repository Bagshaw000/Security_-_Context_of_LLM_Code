import pandas as pd
from datetime import datetime

class AccountingReport:
    def __init__(self, transactions):
        self.transactions = transactions

    def generate_report(self):
        report = self.transactions.groupby('category').agg(
            total_amount=('amount', 'sum'),
            transaction_count=('amount', 'count')
        ).reset_index()
        report['report_date'] = datetime.now().strftime('%Y-%m-%d')
        return report

    def save_report(self, report, filename='accounting_report.csv'):
        report.to_csv(filename, index=False)

def main():
    data = {
        'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
        'amount': [100, -50, 200, -30],
        'category': ['income', 'expense', 'income', 'expense']
    }
    
    transactions = pd.DataFrame(data)
    report_generator = AccountingReport(transactions)
    report = report_generator.generate_report()
    report_generator.save_report(report)

if __name__ == "__main__":
    main()