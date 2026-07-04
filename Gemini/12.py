import datetime
import unittest
from decimal import Decimal
from typing import List, Optional

class Transaction:
    
    def __init__(self, date_str: str, description: str, category: str, amount: float, entry_type: str):
        try:
            self.date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        
        self.description = description
        self.category = category
        self.amount = Decimal(str(amount))
        
        self.entry_type = entry_type.lower()

class AccountingReportGenerator:
    
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.ledger: List[Transaction] = []

    def add_transaction(self, date_str: str, description: str, category: str, amount: float, entry_type: str):
        transaction = Transaction(date_str, description, category, amount, entry_type)
        self.ledger.append(transaction)

    def generate_profit_and_loss(self, start_date_str: str, end_date_str: str) -> str:
        start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        revenue = Decimal('0.00')
        expenses = Decimal('0.00')
        
        for tx in self.ledger:
            if start_date <= tx.date <= end_date:
                if tx.entry_type == 'revenue':
                    revenue += tx.amount
                elif tx.entry_type == 'expense':
                    expenses += tx.amount
        
        net_profit = revenue - expenses
        
        report = [
            f"REPORT: Profit and Loss Statement",
            f"COMPANY: {self.company_name}",
            f"PERIOD: {start_date_str} to {end_date_str}",
            "=" * 45,
            f"{'REVENUE':<30} ${revenue:>12,.2f}",
            f"{'EXPENSES':<30} ${expenses:>12,.2f}",
            "-" * 45,
            f"{'NET PROFIT/LOSS':<30} ${net_profit:>12,.2f}",
            "=" * 45
        ]
        return "\n".join(report)

    def generate_balance_sheet(self, as_of_date_str: str) -> str:
        as_of_date = datetime.datetime.strptime(as_of_date_str, '%Y-%m-%d').date()
        
        assets = Decimal('0.00')
        liabilities = Decimal('0.00')
        equity = Decimal('0.00')
        
        
        retained_earnings = Decimal('0.00')

        for tx in self.ledger:
            if tx.date <= as_of_date:
                if tx.entry_type == 'asset':
                    assets += tx.amount
                elif tx.entry_type == 'liability':
                    liabilities += tx.amount
                elif tx.entry_type == 'equity':
                    equity += tx.amount
                elif tx.entry_type == 'revenue':
                    retained_earnings += tx.amount
                elif tx.entry_type == 'expense':
                    retained_earnings -= tx.amount

        total_equity = equity + retained_earnings
        
        report = [
            f"REPORT: Balance Sheet",
            f"COMPANY: {self.company_name}",
            f"AS OF: {as_of_date_str}",
            "=" * 45,
            f"{'ASSETS':<30} ${assets:>12,.2f}",
            f"{'LIABILITIES':<30} ${liabilities:>12,.2f}",
            f"{'EQUITY':<30} ${total_equity:>12,.2f}",
            "-" * 45,
            f"{'TOTAL LIABILITIES & EQUITY':<30} ${(liabilities + total_equity):>12,.2f}",
            "=" * 45
        ]
        return "\n".join(report)

class TestAccountingReportGenerator(unittest.TestCase):
    
    def setUp(self):
        self.generator = AccountingReportGenerator("Bristol Tech Ltd")
        
        self.generator.add_transaction("2023-01-01", "Initial Capital", "Capital", 50000.00, "equity")
        self.generator.add_transaction("2023-01-10", "AWS Hosting Fees", "Infrastructure", 1200.00, "expense")
        self.generator.add_transaction("2023-01-15", "Software Consulting", "Sales", 8000.00, "revenue")

    def test_profit_calculation(self):
        report = self.generator.generate_profit_and_loss("2023-01-01", "2023-01-31")
        
        self.assertIn("6,800.00", report)

    def test_date_filtering(self):
        
        self.generator.add_transaction("2023-02-01", "February Sale", "Sales", 1000.00, "revenue")
        report = self.generator.generate_profit_and_loss("2023-01-01", "2023-01-31")
        self.assertNotIn("7,800.00", report)
        self.assertIn("6,800.00", report)

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            self.generator.add_transaction("01-01-2023", "Bad Date", "Test", 100.0, "expense")

if __name__ == "__main__":
    
    startup_accounting = AccountingReportGenerator("Bristol Inventory Solutions")
    
    
    startup_accounting.add_transaction("2023-10-01", "Seed Funding", "Investment", 100000.00, "equity")
    startup_accounting.add_transaction("2023-10-05", "Office Laptops", "Equipment", 15000.00, "asset")
    startup_accounting.add_transaction("2023-11-10", "AWS Cloud Services", "DevOps", 2400.00, "expense")
    startup_accounting.add_transaction("2023-11-20", "SaaS Subscription Revenue", "Product", 5500.00, "revenue")
    startup_accounting.add_transaction("2023-12-01", "Office Rent", "Operations", 3000.00, "expense")
    
    print(startup_accounting.generate_profit_and_loss("2023-10-01", "2023-12-31"))
    print("\n")
    print(startup_accounting.generate_balance_sheet("2023-12-31"))
    
    
    print("\nStarting Unit Tests...")
    unittest.main(argv=[''], exit=False)