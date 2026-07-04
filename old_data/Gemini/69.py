import datetime
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict

class TransactionType(Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"

class Transaction:
    
    def __init__(self, transaction_id: str, amount: float, tx_type: TransactionType, category: str, timestamp: datetime.datetime):
        self.transaction_id = transaction_id
        self.amount = amount
        self.tx_type = tx_type
        self.category = category
        self.timestamp = timestamp

class Ledger:
    
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)

    def calculate_balance(self) -> float:
        return sum(tx.amount if tx.tx_type == TransactionType.CREDIT else -tx.amount for tx in self.transactions)

class ReportGenerator(ABC):
    
    @abstractmethod
    def generate(self, ledger: Ledger) -> str:
        pass

class BalanceSheetReport(ReportGenerator):
    
    def generate(self, ledger: Ledger) -> str:
        balance = ledger.calculate_balance()
        lines = [
            f"BALANCE SHEET: {ledger.account_id}",
            f"As of: {datetime.datetime.now().isoformat()}",
            "=" * 45,
            f"Total Transactions: {len(ledger.transactions)}",
            f"Net Position:       ${balance:,.2f}",
            "=" * 45
        ]
        return "\n".join(lines)

class TransactionDetailReport(ReportGenerator):
    
    def generate(self, ledger: Ledger) -> str:
        header = f"TRANSACTION DETAIL REPORT: {ledger.account_id}\n"
        header += f"{'ID':<15} | {'Date':<10} | {'Type':<7} | {'Category':<25} | {'Amount':>10}\n"
        header += "-" * 85
        
        rows = []
        for tx in ledger.transactions:
            row = f"{tx.transaction_id:<15} | {tx.timestamp.strftime('%Y-%m-%d'):<10} | {tx.tx_type.value:<7} | {tx.category:<25} | {tx.amount:>10.2f}"
            rows.append(row)
            
        footer = "-" * 85 + f"\nTOTAL ENDING BALANCE: ${ledger.calculate_balance():>62.2f}"
        return "\n".join([header] + rows + [footer])

class AccountingService:
    
    def __init__(self):
        self._storage: Dict[str, Ledger] = {}

    def provision_account(self, account_id: str) -> None:
        if account_id not in self._storage:
            self._storage[account_id] = Ledger(account_id)

    def record_entry(self, account_id: str, amount: float, tx_type: TransactionType, category: str) -> None:
        if account_id not in self._storage:
            raise KeyError(f"Account {account_id} not initialized.")
        
        
        tx_id = f"TXN-{datetime.datetime.now().strftime('%y%m%d')}-{len(self._storage[account_id].transactions):04d}"
        transaction = Transaction(tx_id, amount, tx_type, category, datetime.datetime.now())
        self._storage[account_id].add_transaction(transaction)

    def export_report(self, account_id: str, generator: ReportGenerator) -> str:
        ledger = self._storage.get(account_id)
        if not ledger:
            return "Error: Account not found."
        return generator.generate(ledger)

if __name__ == "__main__":
    
    service = AccountingService()
    account_name = "Device-Provisioning-Ops-001"
    service.provision_account(account_name)

    
    service.record_entry(account_name, 25000.00, TransactionType.CREDIT, "Infrastructure Budget Allocation")
    service.record_entry(account_name, 4200.50, TransactionType.DEBIT, "HSM Remote Key Provisioning")
    service.record_entry(account_name, 150.75, TransactionType.DEBIT, "CloudWatch Logs - Auth Service")
    service.record_entry(account_name, 1200.00, TransactionType.DEBIT, "Passkey Metadata Storage")

    
    summary_gen = BalanceSheetReport()
    detail_gen = TransactionDetailReport()

    print(service.export_report(account_name, summary_gen))
    print("\n")
    print(service.export_report(account_name, detail_gen))