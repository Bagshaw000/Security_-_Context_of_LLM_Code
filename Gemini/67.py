import logging
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto
from typing import List, Dict, Optional
from dataclasses import dataclass, field


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AccountType(Enum):
    ASSET = auto()
    LIABILITY = auto()
    EQUITY = auto()
    REVENUE = auto()
    EXPENSE = auto()

class EntryType(Enum):
    DEBIT = auto()
    CREDIT = auto()

@dataclass(frozen=True)
class JournalEntry:
    account_id: str
    amount: Decimal
    entry_type: EntryType
    timestamp: datetime = field(default_factory=datetime.utcnow)
    description: str = ""

@dataclass
class Account:
    account_id: str
    name: str
    account_type: AccountType
    entries: List[JournalEntry] = field(default_factory=list)

    def get_balance(self) -> Decimal:
        
        debits = sum(e.amount for e in self.entries if e.entry_type == EntryType.DEBIT)
        credits = sum(e.amount for e in self.entries if e.entry_type == EntryType.CREDIT)

        if self.account_type in (AccountType.ASSET, AccountType.EXPENSE):
            return debits - credits
        else:
            return credits - debits

class GeneralLedger:
    def __init__(self):
        self._accounts: Dict[str, Account] = {}

    def add_account(self, account: Account):
        if account.account_id in self._accounts:
            raise ValueError(f"Account {account.account_id} already exists.")
        self._accounts[account.account_id] = account

    def record_transaction(self, debit_acc_id: str, credit_acc_id: str, amount: Decimal, description: str):
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")
        
        timestamp = datetime.utcnow()
        
        debit_entry = JournalEntry(debit_acc_id, amount, EntryType.DEBIT, timestamp, description)
        credit_entry = JournalEntry(credit_acc_id, amount, EntryType.CREDIT, timestamp, description)

        self._accounts[debit_acc_id].entries.append(debit_entry)
        self._accounts[credit_acc_id].entries.append(credit_entry)
        
        logger.info(f"Recorded transaction: {description} | Amount: {amount}")

    def get_accounts_by_type(self, account_type: AccountType) -> List[Account]:
        return [acc for acc in self._accounts.values() if acc.account_type == account_type]

class ReportGenerator:
    
    def __init__(self, ledger: GeneralLedger):
        self.ledger = ledger

    def generate_profit_and_loss(self) -> str:
        revenues = self.ledger.get_accounts_by_type(AccountType.REVENUE)
        expenses = self.ledger.get_accounts_by_type(AccountType.EXPENSE)

        total_revenue = sum(acc.get_balance() for acc in revenues)
        total_expense = sum(acc.get_balance() for acc in expenses)
        net_income = total_revenue - total_expense

        lines = [
            "--- PROFIT AND LOSS STATEMENT ---",
            f"Generated at: {datetime.now().isoformat()}",
            "\nREVENUE:"
        ]
        for acc in revenues:
            lines.append(f"  {acc.name:20}: {acc.get_balance():>12.2f}")
        
        lines.append(f"TOTAL REVENUE:       {total_revenue:>12.2f}")
        lines.append("\nEXPENSES:")
        
        for acc in expenses:
            lines.append(f"  {acc.name:20}: {acc.get_balance():>12.2f}")
            
        lines.append(f"TOTAL EXPENSES:      {total_expense:>12.2f}")
        lines.append("-" * 33)
        lines.append(f"NET INCOME:          {net_income:>12.2f}")
        lines.append("-" * 33)
        
        return "\n".join(lines)

    def generate_balance_sheet(self) -> str:
        assets = self.ledger.get_accounts_by_type(AccountType.ASSET)
        liabilities = self.ledger.get_accounts_by_type(AccountType.LIABILITY)
        equity = self.ledger.get_accounts_by_type(AccountType.EQUITY)

        total_assets = sum(acc.get_balance() for acc in assets)
        total_liabilities = sum(acc.get_balance() for acc in liabilities)
        total_equity = sum(acc.get_balance() for acc in equity)

        lines = [
            "--- BALANCE SHEET ---",
            f"Date: {datetime.now().date().isoformat()}",
            "\nASSETS:"
        ]
        for acc in assets:
            lines.append(f"  {acc.name:20}: {acc.get_balance():>12.2f}")
        lines.append(f"TOTAL ASSETS:        {total_assets:>12.2f}")

        lines.append("\nLIABILITIES:")
        for acc in liabilities:
            lines.append(f"  {acc.name:20}: {acc.get_balance():>12.2f}")
        lines.append(f"TOTAL LIABILITIES:   {total_liabilities:>12.2f}")

        lines.append("\nEQUITY:")
        for acc in equity:
            lines.append(f"  {acc.name:20}: {acc.get_balance():>12.2f}")
        lines.append(f"TOTAL EQUITY:        {total_equity:>12.2f}")
        
        lines.append("-" * 33)
        lines.append(f"LIABILITIES + EQUITY: {(total_liabilities + total_equity):>12.2f}")
        lines.append("-" * 33)

        return "\n".join(lines)

def main():
    
    ledger = GeneralLedger()

    
    ledger.add_account(Account("101", "Cash", AccountType.ASSET))
    ledger.add_account(Account("102", "Accounts Receivable", AccountType.ASSET))
    ledger.add_account(Account("201", "Accounts Payable", AccountType.LIABILITY))
    ledger.add_account(Account("301", "Owner's Equity", AccountType.EQUITY))
    ledger.add_account(Account("401", "Service Revenue", AccountType.REVENUE))
    ledger.add_account(Account("501", "Rent Expense", AccountType.EXPENSE))
    ledger.add_account(Account("502", "Cloud Infrastructure", AccountType.EXPENSE))

    
    try:
        
        ledger.record_transaction("101", "301", Decimal("50000.00"), "Initial capital injection")
        
        
        ledger.record_transaction("101", "401", Decimal("12000.00"), "Q1 Software Consulting")
        
        
        ledger.record_transaction("501", "101", Decimal("2500.00"), "Office Rent")
        ledger.record_transaction("502", "101", Decimal("1500.75"), "AWS Bill - Production Cluster")
        
        
        ledger.record_transaction("502", "201", Decimal("500.00"), "AWS Bill - Pending Payment")

        
        reporter = ReportGenerator(ledger)
        
        print(reporter.generate_profit_and_loss())
        print("\n")
        print(reporter.generate_balance_sheet())

    except Exception as e:
        logger.error(f"Failed to process accounting data: {e}")

if __name__ == "__main__":
    main()