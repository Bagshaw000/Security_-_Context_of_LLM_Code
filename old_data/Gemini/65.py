import dataclasses
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict, Optional
from decimal import Decimal, ROUND_HALF_UP

class AccountType(Enum):
    ASSET = auto()
    LIABILITY = auto()
    EQUITY = auto()
    REVENUE = auto()
    EXPENSE = auto()

@dataclasses.dataclass(frozen=True)
class Transaction:
    
    transaction_id: str
    timestamp: datetime
    description: str
    amount: Decimal
    account_type: AccountType

class FinancialLedger:
    
    def __init__(self):
        self._transactions: List[Transaction] = []

    def record_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def get_transactions_by_type(self, account_type: AccountType) -> List[Transaction]:
        return [t for t in self._transactions if t.account_type == account_type]

    def calculate_total(self, account_type: AccountType) -> Decimal:
        total = sum((t.amount for t in self.get_transactions_by_type(account_type)), Decimal('0.00'))
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class ReportGenerator:
    
    def __init__(self, ledger: FinancialLedger):
        self.ledger = ledger

    def generate_income_statement(self) -> str:
        revenue = self.ledger.calculate_total(AccountType.REVENUE)
        expenses = self.ledger.calculate_total(AccountType.EXPENSE)
        net_income = revenue - expenses

        lines = [
            "========================================",
            "           INCOME STATEMENT             ",
            f"           As of {datetime.now().strftime('%Y-%m-%d')}       ",
            "========================================",
            f"REVENUE:             {revenue:>15}",
            f"OPERATING EXPENSES:  {expenses:>15}",
            "----------------------------------------",
            f"NET INCOME:          {net_income:>15}",
            "========================================"
        ]
        return "\n".join(lines)

    def generate_balance_sheet(self) -> str:
        assets = self.ledger.calculate_total(AccountType.ASSET)
        liabilities = self.ledger.calculate_total(AccountType.LIABILITY)
        equity = self.ledger.calculate_total(AccountType.EQUITY)
        
        
        balance_check = assets == (liabilities + equity)

        lines = [
            "========================================",
            "            BALANCE SHEET               ",
            f"           As of {datetime.now().strftime('%Y-%m-%d')}       ",
            "========================================",
            f"ASSETS:              {assets:>15}",
            f"LIABILITIES:         {liabilities:>15}",
            f"EQUITY:              {equity:>15}",
            "----------------------------------------",
            f"TOTAL L + E:         {(liabilities + equity):>15}",
            f"BALANCED:            {str(balance_check):>15}",
            "========================================"
        ]
        return "\n".join(lines)

def run_accounting_service_demo():
    
    ledger = FinancialLedger()

    
    ledger.record_transaction(Transaction("tx-001", datetime.now(), "AWS Cloud Services Sales", Decimal("25000.00"), AccountType.REVENUE))
    ledger.record_transaction(Transaction("tx-002", datetime.now(), "Hardware Manufacturing Costs", Decimal("12000.00"), AccountType.EXPENSE))
    ledger.record_transaction(Transaction("tx-003", datetime.now(), "Cash Reserves", Decimal("50000.00"), AccountType.ASSET))
    ledger.record_transaction(Transaction("tx-004", datetime.now(), "Accounts Payable - Vendors", Decimal("15000.00"), AccountType.LIABILITY))
    ledger.record_transaction(Transaction("tx-005", datetime.now(), "Retained Earnings", Decimal("35000.00"), AccountType.EQUITY))

    report_engine = ReportGenerator(ledger)

    
    print(report_engine.generate_income_statement())
    print("\n")
    print(report_engine.generate_balance_sheet())

if __name__ == "__main__":
    run_accounting_service_demo()