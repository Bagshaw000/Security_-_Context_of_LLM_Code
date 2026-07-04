import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, auto
from typing import List, Dict, Optional


class AccountType(Enum):
    ASSET = auto()
    LIABILITY = auto()
    EQUITY = auto()
    REVENUE = auto()
    EXPENSE = auto()


@dataclass(frozen=True)
class JournalEntry:
    account_id: str
    amount: Decimal  
    description: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)


@dataclass
class Account:
    account_id: str
    name: str
    account_type: AccountType
    balance: Decimal = Decimal("0.00")

    def update_balance(self, amount: Decimal):
        self.balance += amount


class AccountingSystem:
    
    def __init__(self):
        self.chart_of_accounts: Dict[str, Account] = {}
        self.ledger: List[JournalEntry] = []

    def add_account(self, account: Account):
        if account.account_id in self.chart_of_accounts:
            raise ValueError(f"Account {account.account_id} already exists.")
        self.chart_of_accounts[account.account_id] = account

    def post_transaction(self, entries: List[JournalEntry]):
        
        if sum(e.amount for e in entries) != Decimal("0.00"):
            raise ValueError("Transaction is not balanced. Debits must equal Credits.")

        for entry in entries:
            if entry.account_id not in self.chart_of_accounts:
                raise ValueError(f"Account {entry.account_id} does not exist.")
            
            self.chart_of_accounts[entry.account_id].update_balance(entry.amount)
            self.ledger.append(entry)


class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, system: AccountingSystem) -> str:
        pass


class BalanceSheetGenerator(ReportGenerator):
    def generate(self, system: AccountingSystem) -> str:
        assets = [a for a in system.chart_of_accounts.values() if a.account_type == AccountType.ASSET]
        liabilities = [a for a in system.chart_of_accounts.values() if a.account_type == AccountType.LIABILITY]
        equity = [a for a in system.chart_of_accounts.values() if a.account_type == AccountType.EQUITY]

        total_assets = sum(a.balance for a in assets)
        total_liabilities = sum(a.balance for a in liabilities)
        total_equity = sum(a.balance for a in equity)

        report = [
            "--- BALANCE SHEET ---",
            f"Generated on: {datetime.date.today()}",
            "\nASSETS:",
        ]
        for a in assets:
            report.append(f"  {a.name:20} : {a.balance:>12}")
        report.append(f"Total Assets: {total_assets:>20}")

        report.append("\nLIABILITIES & EQUITY:")
        for l in liabilities:
            report.append(f"  {l.name:20} : {abs(l.balance):>12}")
        for e in equity:
            report.append(f"  {e.name:20} : {abs(e.balance):>12}")
        
        report.append(f"Total Liab & Equity: {abs(total_liabilities + total_equity):>13}")
        return "\n".join(report)


class IncomeStatementGenerator(ReportGenerator):
    def generate(self, system: AccountingSystem) -> str:
        revenues = [a for a in system.chart_of_accounts.values() if a.account_type == AccountType.REVENUE]
        expenses = [a for a in system.chart_of_accounts.values() if a.account_type == AccountType.EXPENSE]

        
        total_rev = sum(abs(a.balance) for a in revenues)
        total_exp = sum(a.balance for a in expenses)
        net_income = total_rev - total_exp

        report = [
            "--- INCOME STATEMENT ---",
            f"Period ending: {datetime.date.today()}",
            "\nREVENUE:",
        ]
        for r in revenues:
            report.append(f"  {r.name:20} : {abs(r.balance):>12}")
        report.append(f"Total Revenue: {total_rev:>19}")

        report.append("\nEXPENSES:")
        for e in expenses:
            report.append(f"  {e.name:20} : {e.balance:>12}")
        report.append(f"Total Expenses: {total_exp:>18}")
        
        report.append("-" * 35)
        report.append(f"NET INCOME: {net_income:>22}")
        return "\n".join(report)


def main():
    
    sys = AccountingSystem()

    
    sys.add_account(Account("101", "Cash", AccountType.ASSET))
    sys.add_account(Account("102", "Accounts Receivable", AccountType.ASSET))
    sys.add_account(Account("201", "Accounts Payable", AccountType.LIABILITY))
    sys.add_account(Account("301", "Retained Earnings", AccountType.EQUITY))
    sys.add_account(Account("401", "Service Revenue", AccountType.REVENUE))
    sys.add_account(Account("501", "Server Hosting Fees", AccountType.EXPENSE))

    
    
    sys.post_transaction([
        JournalEntry("101", Decimal("50000.00"), "Initial Capital Injection"),
        JournalEntry("301", Decimal("-50000.00"), "Initial Capital Injection")
    ])

    
    sys.post_transaction([
        JournalEntry("102", Decimal("15000.00"), "Cloud Service Invoice 
        JournalEntry("401", Decimal("-15000.00"), "Cloud Service Invoice 
    ])

    
    sys.post_transaction([
        JournalEntry("501", Decimal("2500.00"), "AWS Infrastructure Cost"),
        JournalEntry("101", Decimal("-2500.00"), "AWS Infrastructure Cost")
    ])

    
    bs_gen = BalanceSheetGenerator()
    is_gen = IncomeStatementGenerator()

    print(is_gen.generate(sys))
    print("\n")
    print(bs_gen.generate(sys))


if __name__ == "__main__":
    main()