import json
import unittest
from datetime import datetime
from decimal import Decimal
from collections import defaultdict

class Transaction:
    
    def __init__(self, date, description, category, amount, transaction_type):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.description = description
        self.category = category
        self.amount = Decimal(str(amount))
        self.transaction_type = transaction_type  

class AccountingReportGenerator:
    
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def generate_profit_loss_report(self):
        total_income = sum(t.amount for t in self.transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        net_profit = total_income - total_expenses

        return {
            "report_type": "Profit and Loss",
            "generated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "summary": {
                "total_income": float(total_income),
                "total_expenses": float(total_expenses),
                "net_profit": float(net_profit)
            }
        }

    def generate_expense_breakdown(self):
        breakdown = defaultdict(Decimal)
        for t in self.transactions:
            if t.transaction_type == 'expense':
                breakdown[t.category] += t.amount
        
        return {category: float(amount) for category, amount in breakdown.items()}

class AWSReportUploader:
    
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

    def upload_to_s3(self, report_data, file_name):
        
        payload = json.dumps(report_data)
        print(f"DEBUG: Uploading {file_name} to S3 bucket: {self.bucket_name}")
        
        return True

class TestAccountingReports(unittest.TestCase):
    
    def setUp(self):
        self.generator = AccountingReportGenerator()
        self.generator.add_transaction(Transaction("2023-12-01", "Client Project A", "Consulting", 5000.00, "income"))
        self.generator.add_transaction(Transaction("2023-12-02", "Monthly AWS Bill", "Infrastructure", 150.50, "expense"))
        self.generator.add_transaction(Transaction("2023-12-05", "Office Supplies", "Operations", 49.50, "expense"))

    def test_net_profit_calculation(self):
        report = self.generator.generate_profit_loss_report()
        self.assertEqual(report["summary"]["net_profit"], 4800.00)

    def test_expense_breakdown(self):
        breakdown = self.generator.generate_expense_breakdown()
        self.assertEqual(breakdown["Infrastructure"], 150.50)
        self.assertEqual(breakdown["Operations"], 49.50)

def main():
    
    report_gen = AccountingReportGenerator()
    
    
    report_gen.add_transaction(Transaction("2024-01-01", "SaaS Subscription Revenue", "Sales", 12000.00, "income"))
    report_gen.add_transaction(Transaction("2024-01-05", "Engineering Salaries", "Payroll", 8000.00, "expense"))
    report_gen.add_transaction(Transaction("2024-01-10", "Cloud Hosting", "Infrastructure", 500.00, "expense"))

    
    pl_report = report_gen.generate_profit_loss_report()
    expense_report = report_gen.generate_expense_breakdown()

    
    print("--- Financial Report Summary ---")
    print(json.dumps(pl_report, indent=2))
    print("\n--- Expense Breakdown by Category ---")
    print(json.dumps(expense_report, indent=2))

    
    uploader = AWSReportUploader(bucket_name="fin-reports-storage-prod")
    uploader.upload_to_s3(pl_report, "january_2024_pl.json")

if __name__ == "__main__":
    
    main()
    
    
    print("\nStarting Unit Tests...")
    unittest.main(argv=[''], exit=False)