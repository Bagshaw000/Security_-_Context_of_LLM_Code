import json
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict
import unittest

class Transaction:
    
    def __init__(self, date_str, description, category, amount, entry_type):
        self.date = datetime.strptime(date_str, '%Y-%m-%d')
        self.description = description
        self.category = category
        self.amount = Decimal(str(amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        self.entry_type = entry_type.upper()

    def to_dict(self):
        return {
            "date": self.date.strftime('%Y-%m-%d'),
            "description": self.description,
            "category": self.category,
            "amount": float(self.amount),
            "type": self.entry_type
        }

class Ledger:
    
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions_in_range(self, start_date, end_date):
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        return [t for t in self.transactions if start <= t.date <= end]

class ReportEngine:
    
    def __init__(self, ledger):
        self.ledger = ledger

    def generate_profit_and_loss(self, start_date, end_date):
        
        data = self.ledger.get_transactions_in_range(start_date, end_date)
        
        report = {
            "period": f"{start_date} to {end_date}",
            "revenue": Decimal('0.00'),
            "expenses": Decimal('0.00'),
            "net_income": Decimal('0.00'),
            "expense_breakdown": defaultdict(Decimal),
            "revenue_breakdown": defaultdict(Decimal)
        }

        for t in data:
            if t.entry_type == 'CREDIT':
                report["revenue"] += t.amount
                report["revenue_breakdown"][t.category] += t.amount
            elif t.entry_type == 'DEBIT':
                report["expenses"] += t.amount
                report["expense_breakdown"][t.category] += t.amount

        report["net_income"] = report["revenue"] - report["expenses"]
        return report

    def generate_inventory_valuation_report(self, inventory_items):
        
        total_value = Decimal('0.00')
        valuation_details = []
        
        for item in inventory_items:
            item_total = Decimal(str(item['quantity'])) * Decimal(str(item['unit_cost']))
            total_value += item_total
            valuation_details.append({
                "sku": item['sku'],
                "valuation": float(item_total)
            })
            
        return {
            "total_inventory_value": float(total_value),
            "items": valuation_details
        }

class TestAccountingSystem(unittest.TestCase):
    
    
    def setUp(self):
        self.ledger = Ledger()
        
        self.ledger.add_transaction(Transaction('2023-01-01', 'Widget Sale', 'Sales', 1500.00, 'CREDIT'))
        self.ledger.add_transaction(Transaction('2023-01-05', 'Warehouse Rent', 'Rent', 800.00, 'DEBIT'))
        self.ledger.add_transaction(Transaction('2023-01-10', 'Office Supplies', 'Supplies', 50.25, 'DEBIT'))
        self.engine = ReportEngine(self.ledger)

    def test_net_income_calculation(self):
        report = self.engine.generate_profit_and_loss('2023-01-01', '2023-01-31')
        expected_net = Decimal('1500.00') - (Decimal('800.00') + Decimal('50.25'))
        self.assertEqual(report["net_income"], expected_net)

    def test_date_filtering(self):
        report = self.engine.generate_profit_and_loss('2023-02-01', '2023-02-28')
        self.assertEqual(report["revenue"], Decimal('0.00'))

    def test_inventory_valuation(self):
        items = [
            {'sku': 'WDG-01', 'quantity': 10, 'unit_cost': 5.00},
            {'sku': 'WDG-02', 'quantity': 5, 'unit_cost': 20.00}
        ]
        report = self.engine.generate_inventory_valuation_report(items)
        self.assertEqual(report["total_inventory_value"], 150.00)

def run_sample_report():
    
    my_ledger = Ledger()
    
    
    tx_data = [
        ('2023-11-01', 'Consulting Fee', 'Service Revenue', 5000.00, 'CREDIT'),
        ('2023-11-02', 'Cloud Server Hosting', 'IT Infrastructure', 120.50, 'DEBIT'),
        ('2023-11-15', 'Monthly Inventory Restock', 'COGS', 1200.00, 'DEBIT'),
        ('2023-11-20', 'Software License', 'SaaS', 45.00, 'DEBIT')
    ]
    
    for date, desc, cat, amt, typ in tx_data:
        my_ledger.add_transaction(Transaction(date, desc, cat, amt, typ))
    
    
    engine = ReportEngine(my_ledger)
    p_and_l = engine.generate_profit_and_loss('2023-11-01', '2023-11-30')
    
    
    print("--- PROFIT AND LOSS STATEMENT ---")
    print(f"Period: {p_and_l['period']}")
    print(f"Total Revenue:  ${p_and_l['revenue']:>10}")
    print(f"Total Expenses: ${p_and_l['expenses']:>10}")
    print("-" * 33)
    print(f"Net Income:     ${p_and_l['net_income']:>10}")
    print("\nExpense Breakdown:")
    for cat, amt in p_and_l['expense_breakdown'].items():
        print(f" - {cat}: ${amt}")

if __name__ == "__main__":
    
    print("Running Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountingSystem)
    unittest.TextTestRunner(verbosity=1).run(suite)
    print("\n" + "="*40 + "\n")
    
    
    run_sample_report()