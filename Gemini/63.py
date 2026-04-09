import json
import unittest
from datetime import datetime
from typing import List, Dict, Any

class Transaction:
    
    def __init__(self, date: str, description: str, amount: float, category: str, entry_type: str):
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.description = description
        self.amount = amount
        self.category = category
        self.entry_type = entry_type.lower()  

class AccountingReportGenerator:
    
    def __init__(self):
        self.transactions: List[Transaction] = []

    def add_transaction(self, date: str, description: str, amount: float, category: str, entry_type: str):
        if entry_type.lower() not in ['income', 'expense']:
            raise ValueError("Entry type must be 'income' or 'expense'")
        
        transaction = Transaction(date, description, amount, category, entry_type)
        self.transactions.append(transaction)

    def calculate_summary(self) -> Dict[str, Any]:
        total_income = sum(t.amount for t in self.transactions if t.entry_type == 'income')
        total_expenses = sum(t.amount for t in self.transactions if t.entry_type == 'expense')
        net_profit = total_income - total_expenses

        
        category_breakdown = {}
        for t in self.transactions:
            if t.category not in category_breakdown:
                category_breakdown[t.category] = 0.0
            
            if t.entry_type == 'income':
                category_breakdown[t.category] += t.amount
            else:
                category_breakdown[t.category] -= t.amount

        return {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "transaction_count": len(self.transactions)
            },
            "totals": {
                "gross_income": round(total_income, 2),
                "total_expenses": round(total_expenses, 2),
                "net_profit": round(net_profit, 2)
            },
            "category_breakdown": {k: round(v, 2) for k, v in category_breakdown.items()}
        }

    def export_json_report(self) -> str:
        return json.dumps(self.calculate_summary(), indent=4)

class TestAccountingReport(unittest.TestCase):
    
    
    def setUp(self):
        self.generator = AccountingReportGenerator()

    def test_add_transaction_valid(self):
        self.generator.add_transaction("2023-01-01", "Test Income", 100.0, "Sales", "income")
        self.assertEqual(len(self.generator.transactions), 1)

    def test_invalid_type_raises_error(self):
        with self.assertRaises(ValueError):
            self.generator.add_transaction("2023-01-01", "Test", 10.0, "Misc", "invalid")

    def test_net_profit_calculation(self):
        self.generator.add_transaction("2023-05-01", "Client A Payment", 5000.0, "Revenue", "income")
        self.generator.add_transaction("2023-05-02", "AWS Hosting", 200.0, "Infrastructure", "expense")
        self.generator.add_transaction("2023-05-03", "Office Supplies", 50.0, "Admin", "expense")
        
        summary = self.generator.calculate_summary()
        self.assertEqual(summary["totals"]["net_profit"], 4750.0)
        self.assertEqual(summary["category_breakdown"]["Infrastructure"], -200.0)

def main():
    
    report_gen = AccountingReportGenerator()
    
    
    report_gen.add_transaction("2023-10-01", "Inventory Sale - SKU 402", 1200.50, "Sales", "income")
    report_gen.add_transaction("2023-10-02", "Monthly AWS Bill", 145.20, "Cloud Services", "expense")
    report_gen.add_transaction("2023-10-05", "Warehouse Rent", 800.00, "Fixed Costs", "expense")
    report_gen.add_transaction("2023-10-10", "Inventory Restock", 450.00, "COGS", "expense")

    print("Generating Accounting Report...")
    print(report_gen.export_json_report())

if __name__ == "__main__":
    
    main()
    
    
    print("\nRunning unit tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAccountingReport)
    unittest.TextTestRunner(verbosity=1).run(suite)