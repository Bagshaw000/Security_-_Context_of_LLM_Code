import datetime
from decimal import Decimal
from collections import defaultdict
import unittest

class Transaction:
    
    def __init__(self, date_str, description, amount, category, account_type):
        self.date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        self.description = description
        self.amount = Decimal(str(amount))
        self.category = category
        self.account_type = account_type  

class AccountingReportGenerator:
    
    def __init__(self, company_name):
        self.company_name = company_name
        self.ledger = []

    def add_transaction(self, transaction):
        
        self.ledger.append(transaction)

    def generate_profit_and_loss(self, start_date_str, end_date_str):
        
        start = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        
        report = {
            "Revenue": defaultdict(Decimal),
            "Expenses": defaultdict(Decimal),
            "Total Revenue": Decimal("0.00"),
            "Total Expenses": Decimal("0.00")
        }

        for tx in self.ledger:
            if start <= tx.date <= end:
                if tx.account_type == "Revenue":
                    report["Revenue"][tx.category] += tx.amount
                    report["Total Revenue"] += tx.amount
                elif tx.account_type == "Expense":
                    report["Expenses"][tx.category] += tx.amount
                    report["Total Expenses"] += tx.amount

        report["Net Income"] = report["Total Revenue"] - report["Total Expenses"]
        return report

    def format_text_report(self, report_data, start_date, end_date):
        
        output = [
            f"ACCOUNTING REPORT: {self.company_name}",
            f"Period: {start_date} to {end_date}",
            "-" * 40,
            "REVENUE:"
        ]
        
        for cat, amt in report_data["Revenue"].items():
            output.append(f"  {cat:.<25} ${amt:>10,.2f}")
        output.append(f"TOTAL REVENUE: {'.' * 11} ${report_data['Total Revenue']:>10,.2f}")
        
        output.append("\nEXPENSES:")
        for cat, amt in report_data["Expenses"].items():
            output.append(f"  {cat:.<25} ${amt:>10,.2f}")
        output.append(f"TOTAL EXPENSES: {'.' * 10} ${report_data['Total Expenses']:>10,.2f}")
        
        output.append("-" * 40)
        output.append(f"NET INCOME: {'.' * 14} ${report_data['Net Income']:>10,.2f}")
        
        return "\n".join(output)

class TestAccountingSystem(unittest.TestCase):
    
    def setUp(self):
        self.engine = AccountingReportGenerator("Bristol Software Ltd")

    def test_profit_calculation(self):
        self.engine.add_transaction(Transaction("2023-12-01", "Client Payment", "2000.00", "Services", "Revenue"))
        self.engine.add_transaction(Transaction("2023-12-05", "AWS Hosting", "150.00", "Infrastructure", "Expense"))
        
        report = self.engine.generate_profit_and_loss("2023-12-01", "2023-12-31")
        self.assertEqual(report["Net Income"], Decimal("1850.00"))

    def test_out_of_range_ignored(self):
        self.engine.add_transaction(Transaction("2023-11-01", "Old Sale", "100.00", "Services", "Revenue"))
        report = self.engine.generate_profit_and_loss("2023-12-01", "2023-12-31")
        self.assertEqual(report["Total Revenue"], Decimal("0.00"))

if __name__ == "__main__":
    
    reporter = AccountingReportGenerator("Bristol Inventory Solutions")
    
    
    reporter.add_transaction(Transaction("2024-01-10", "SaaS Licensing", "5500.00", "Software Sales", "Revenue"))
    reporter.add_transaction(Transaction("2024-01-15", "AWS CloudFront/S3", "342.50", "Infrastructure", "Expense"))
    reporter.add_transaction(Transaction("2024-01-20", "GitHub Enterprise", "120.00", "Dev Tools", "Expense"))
    reporter.add_transaction(Transaction("2024-01-25", "Consulting Fee", "1200.00", "Services", "Revenue"))

    
    start, end = "2024-01-01", "2024-01-31"
    pl_data = reporter.generate_profit_and_loss(start, end)
    print(reporter.format_text_report(pl_data, start, end))
    
    
    print("\n" + "="*40)
    print("RUNNING INTERNAL UNIT TESTS")
    print("="*40)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountingSystem)
    unittest.TextTestRunner(verbosity=1).run(suite)