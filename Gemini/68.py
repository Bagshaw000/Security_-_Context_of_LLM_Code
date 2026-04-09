import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass

class AccountType(Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    EQUITY = "EQUITY"
    REVENUE = "REVENUE"
    EXPENSE = "EXPENSE"

@dataclass(frozen=True)
class Transaction:
    
    transaction_id: str
    account_name: str
    account_type: AccountType
    amount: Decimal
    timestamp: datetime.datetime
    description: str

class AccountingReportEngine:
    
    def __init__(self):
        self._ledger: List[Transaction] = []

    def record_entry(self, transaction: Transaction) -> None:
        
        self._ledger.append(transaction)

    def get_trial_balance(self) -> Dict[str, Decimal]:
        
        balances: Dict[str, Decimal] = {}
        for tx in self._ledger:
            balances[tx.account_name] = balances.get(tx.account_name, Decimal('0.00')) + tx.amount
        return balances

    def generate_profit_and_loss(self, start_date: datetime.datetime, end_date: datetime.datetime) -> Dict[str, Decimal]:
        
        revenue = Decimal('0.00')
        expenses = Decimal('0.00')

        for tx in self._ledger:
            if start_date <= tx.timestamp <= end_date:
                if tx.account_type == AccountType.REVENUE:
                    revenue += tx.amount
                elif tx.account_type == AccountType.EXPENSE:
                    expenses += tx.amount

        return {
            "Total Revenue": revenue,
            "Total Expenses": expenses,
            "Net Income": revenue - expenses
        }

    def generate_balance_sheet(self) -> Dict[str, Decimal]:
        
        assets = Decimal('0.00')
        liabilities = Decimal('0.00')
        equity = Decimal('0.00')

        for tx in self._ledger:
            if tx.account_type == AccountType.ASSET:
                assets += tx.amount
            elif tx.account_type == AccountType.LIABILITY:
                liabilities += tx.amount
            elif tx.account_type == AccountType.EQUITY:
                equity += tx.amount

        return {
            "Total Assets": assets,
            "Total Liabilities": liabilities,
            "Total Equity": equity,
            "Check (A - L - E)": assets - (liabilities + equity)
        }

def run_demonstration():
    
    engine = AccountingReportEngine()
    now = datetime.datetime.now(datetime.timezone.utc)

    
    engine.record_entry(Transaction("TXN-001", "Cash", AccountType.ASSET, Decimal('10000.00'), now, "Seed Funding"))
    engine.record_entry(Transaction("TXN-002", "Equity Account", AccountType.EQUITY, Decimal('10000.00'), now, "Owner Investment"))
    
    
    engine.record_entry(Transaction("TXN-003", "SaaS Subscriptions", AccountType.REVENUE, Decimal('2500.00'), now, "Monthly User Subs"))
    engine.record_entry(Transaction("TXN-004", "AWS Infrastructure", AccountType.EXPENSE, Decimal('800.00'), now, "Cloud Compute Costs"))
    engine.record_entry(Transaction("TXN-005", "Office Rent", AccountType.EXPENSE, Decimal('1200.00'), now, "Co-working Space"))

    
    pnl = engine.generate_profit_and_loss(now - datetime.timedelta(days=1), now + datetime.timedelta(days=1))
    balance_sheet = engine.generate_balance_sheet()

    print("--- PROFIT & LOSS STATEMENT ---")
    for key, val in pnl.items():
        print(f"{key:20}: {val:>10.2f}")

    print("\n--- BALANCE SHEET ---")
    for key, val in balance_sheet.items():
        print(f"{key:20}: {val:>10.2f}")

if __name__ == "__main__":
    run_demonstration()