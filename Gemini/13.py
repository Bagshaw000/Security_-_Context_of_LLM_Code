import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Optional

class TransactionType(enum.Enum):
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"

@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    amount: Decimal
    timestamp: datetime
    account_name: str
    tx_type: TransactionType
    description: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Transaction amount must be non-negative. Use TransactionType to denote direction.")

class AccountingLedger:
    
    def __init__(self):
        self._transactions: List[Transaction] = []

    def record_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def get_all_transactions(self) -> List[Transaction]:
        return list(self._transactions)

    def get_transactions_by_type(self, tx_type: TransactionType) -> List[Transaction]:
        return [t for t in self._transactions if t.tx_type == tx_type]

class FinancialReport(ABC):
    @abstractmethod
    def generate(self, ledger: AccountingLedger) -> str:
        pass

class IncomeStatement(FinancialReport):
    
    def generate(self, ledger: AccountingLedger) -> str:
        revenues = ledger.get_transactions_by_type(TransactionType.REVENUE)
        expenses = ledger.get_transactions_by_type(TransactionType.EXPENSE)
        
        total_revenue = sum((t.amount for t in revenues), Decimal("0.00"))
        total_expense = sum((t.amount for t in expenses), Decimal("0.00"))
        net_income = total_revenue - total_expense

        lines = [
            "=== INCOME STATEMENT ===",
            f"Total Revenue:  {total_revenue.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):>15}",
            f"Total Expenses: {total_expense.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):>15}",
            "-" * 30,
            f"Net Income:     {net_income.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):>15}",
            "========================"
        ]
        return "\n".join(lines)

class BalanceSheet(FinancialReport):
    
    def generate(self, ledger: AccountingLedger) -> str:
        assets = sum((t.amount for t in ledger.get_transactions_by_type(TransactionType.ASSET)), Decimal("0.00"))
        liabilities = sum((t.amount for t in ledger.get_transactions_by_type(TransactionType.LIABILITY)), Decimal("0.00"))
        equity = sum((t.amount for t in ledger.get_transactions_by_type(TransactionType.EQUITY)), Decimal("0.00"))
        
        
        revenues = sum((t.amount for t in ledger.get_transactions_by_type(TransactionType.REVENUE)), Decimal("0.00"))
        expenses = sum((t.amount for t in ledger.get_transactions_by_type(TransactionType.EXPENSE)), Decimal("0.00"))
        retained_earnings = revenues - expenses
        
        total_equity = equity + retained_earnings

        lines = [
            "=== BALANCE SHEET ===",
            f"Total Assets:      {assets.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):>15}",
            f"Total Liabilities: {liabilities.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):>15}",
            f"Total Equity:      {total_equity.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):>15}",
            "-" * 30,
            f"L + E Check:       {(liabilities + total_equity).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):>15}",
            "====================="
        ]
        return "\n".join(lines)

class ReportService:
    
    def __init__(self, ledger: AccountingLedger):
        self._ledger = ledger

    def run_report(self, report_type: FinancialReport) -> None:
        print(report_type.generate(self._ledger))
        print("\n")

def main():
    
    ledger = AccountingLedger()
    report_service = ReportService(ledger)

    
    ledger.record_transaction(Transaction("TXN-001", Decimal("15000.00"), datetime.now(), "Cash", TransactionType.ASSET, "Initial Capital"))
    ledger.record_transaction(Transaction("TXN-002", Decimal("5000.00"), datetime.now(), "SaaS Subscriptions", TransactionType.REVENUE, "Monthly Sales"))
    ledger.record_transaction(Transaction("TXN-003", Decimal("1200.50"), datetime.now(), "AWS Infrastructure", TransactionType.EXPENSE, "Cloud Hosting Fees"))
    ledger.record_transaction(Transaction("TXN-004", Decimal("800.00"), datetime.now(), "Office Rent", TransactionType.EXPENSE, "Co-working space"))
    ledger.record_transaction(Transaction("TXN-005", Decimal("2000.00"), datetime.now(), "Business Loan", TransactionType.LIABILITY, "SBA Loan"))

    
    report_service.run_report(IncomeStatement())
    report_service.run_report(BalanceSheet())

if __name__ == "__main__":
    main()