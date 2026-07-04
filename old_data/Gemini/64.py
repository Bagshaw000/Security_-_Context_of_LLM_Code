import datetime
import json
from decimal import Decimal
from typing import List, Dict, Any
from dataclasses import dataclass, asdict
import unittest

@dataclass
class Transaction:
    transaction_id: int
    date: datetime.date
    description: str
    amount: Decimal
    account_type: str  

class ReportGenerator:
    
    def __init__(self, company_name: str):
        self.company_name = company_name
        self.ledger: List[Transaction] = []

    def add_entry(self, date_str: str, description: str, amount: float, account_type: str):
        tx_id = len(self.ledger) + 1
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        transaction = Transaction(
            transaction_id=tx_id,
            date=date_obj,
            description=description,
            amount=Decimal(str(amount)),
            account_type=account_type
        )
        self.ledger.append(transaction)

    def generate_income_statement(self, start_date: datetime.date, end_date: datetime.date) -> Dict[str, Any]:
        revenue = Decimal("0.00")
        expenses = Decimal("0.00")

        for tx in self.ledger:
            if start_date <= tx.date <= end_date:
                if tx.account_type == "Revenue":
                    revenue += tx.amount
                elif tx.account_type == "Expense":
                    expenses += tx.amount

        net_income = revenue - expenses
        
        return {
            "report_type": "Income Statement",
            "company": self.company_name,
            "period": f"{start_date} to {end_date}",
            "total_revenue": float(revenue),
            "total_expenses": float(expenses),
            "net_income": float(net_income)
        }

    def generate_balance_sheet(self, as_of_date: datetime.date) -> Dict[str, Any]:
        assets = Decimal("0.00")
        liabilities = Decimal("0.00")
        equity = Decimal("0.00")

        for tx in self.ledger:
            if tx.date <= as_of_date:
                if tx.account_type == "Asset":
                    assets += tx.amount
                elif tx.account_type == "Liability":
                    liabilities += tx.amount
                elif tx.account_type == "Equity":
                    equity += tx.amount

        return {
            "report_type": "Balance Sheet",
            "as_of": str(as_of_date),
            "assets": float(assets),
            "liabilities": float(liabilities),
            "equity": float(equity),
            "is_balanced": (assets == liabilities + equity)
        }

class CloudExporter:
    
    @staticmethod
    def export_to_s3_mock(report_data: Dict[str, Any], bucket: str):
        file_name = f"reports/{report_data['report_type'].replace(' ', '_')}_{datetime.date.today()}.json"
        
        
        print(f"DEBUG: Uploading report to s3://{bucket}/{file_name}")
        return json.dumps(report_data, indent=4)

class TestAccountingReports(unittest.TestCase):
    
    def setUp(self):
        self.gen = ReportGenerator("Bristol Tech Solutions")
        self.gen.add_entry("2023-01-10", "Software License Sale", 5000.00, "Revenue")
        self.gen.add_entry("2023-01-15", "Server Costs", 1200.00, "Expense")
        self.gen.add_entry("2023-01-20", "Initial Capital", 10000.00, "Equity")
        self.gen.add_entry("2023-01-20", "Cash in Bank", 10000.00, "Asset")

    def test_net_income_calculation(self):
        report = self.gen.generate_income_statement(
            datetime.date(2023, 1, 1), 
            datetime.date(2023, 1, 31)
        )
        self.assertEqual(report["net_income"], 3800.00)

    def test_balance_sheet_integrity(self):
        report = self.gen.generate_balance_sheet(datetime.date(2023, 1, 31))
        self.assertTrue(report["is_balanced"])

def main():
    
    reporter = ReportGenerator("Bristol Tech Solutions")
    
    
    reporter.add_entry("2023-05-01", "Client Consulting Fee", 3000.00, "Revenue")
    reporter.add_entry("2023-05-05", "Office Rent", 1500.00, "Expense")
    reporter.add_entry("2023-05-10", "New Hardware Purchase", 2000.00, "Asset")
    reporter.add_entry("2023-05-10", "Business Loan", 2000.00, "Liability")

    
    income_stmt = reporter.generate_income_statement(
        datetime.date(2023, 5, 1), 
        datetime.date(2023, 5, 31)
    )
    
    balance_sheet = reporter.generate_balance_sheet(datetime.date(2023, 5, 31))

    
    exporter = CloudExporter()
    print("--- Income Statement ---")
    print(exporter.export_to_s3_mock(income_stmt, "accounting-reports-bucket"))
    
    print("\n--- Balance Sheet ---")
    print(exporter.export_to_s3_mock(balance_sheet, "accounting-reports-bucket"))

if __name__ == "__main__":
    
    main()
    
    
    print("\n--- Running Unit Tests ---")
    unittest.main(exit=False)