import hashlib
import threading
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional, List
from enum import Enum

class TransactionType(Enum):
    WITHDRAWAL = "WITHDRAWAL"
    DEPOSIT = "DEPOSIT"
    BALANCE_INQUIRY = "BALANCE_INQUIRY"

class TransactionResult(Enum):
    SUCCESS = "SUCCESS"
    INSUFFICIENT_FUNDS = "INSUFFICIENT_FUNDS"
    INVALID_PIN = "INVALID_PIN"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    COMMUNICATION_ERROR = "COMMUNICATION_ERROR"

class Account:
    def __init__(self, account_id: str, pin: str, initial_balance: Decimal):
        self.account_id = account_id
        self._pin_hash = self._hash_pin(pin)
        self.balance = initial_balance
        self.is_locked = False
        self.lock = threading.Lock()

    def _hash_pin(self, pin: str) -> str:
        return hashlib.sha256(pin.encode()).hexdigest()

    def verify_pin(self, pin: str) -> bool:
        return self._pin_hash == self._hash_pin(pin)

class CentralBankSystem:
    
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CentralBankSystem, cls).__new__(cls)
                cls._instance._accounts: Dict[str, Account] = {}
                cls._instance._transaction_logs: List[dict] = []
        return cls._instance

    def add_account(self, account: Account):
        self._accounts[account.account_id] = account

    def authenticate(self, account_id: str, pin: str) -> bool:
        account = self._accounts.get(account_id)
        if account and not account.is_locked:
            return account.verify_pin(pin)
        return False

    def get_balance(self, account_id: str) -> Decimal:
        return self._accounts[account_id].balance

    def process_transaction(self, account_id: str, amount: Decimal, t_type: TransactionType) -> TransactionResult:
        account = self._accounts.get(account_id)
        if not account:
            return TransactionResult.COMMUNICATION_ERROR

        with account.lock:
            if t_type == TransactionType.WITHDRAWAL:
                if account.balance >= amount:
                    account.balance -= amount
                    self._log_transaction(account_id, t_type, amount, TransactionResult.SUCCESS)
                    return TransactionResult.SUCCESS
                else:
                    return TransactionResult.INSUFFICIENT_FUNDS
            elif t_type == TransactionType.DEPOSIT:
                account.balance += amount
                self._log_transaction(account_id, t_type, amount, TransactionResult.SUCCESS)
                return TransactionResult.SUCCESS
        
        return TransactionResult.COMMUNICATION_ERROR

    def _log_transaction(self, account_id: str, t_type: TransactionType, amount: Decimal, result: TransactionResult):
        log_entry = {
            "transaction_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "account_id": account_id,
            "type": t_type.value,
            "amount": float(amount),
            "result": result.value
        }
        self._transaction_logs.append(log_entry)

class ATMController:
    
    def __init__(self, atm_id: str, bank_system: CentralBankSystem):
        self.atm_id = atm_id
        self.bank_system = bank_system
        self.current_account_id: Optional[str] = None
        self.is_authenticated = False

    def insert_card(self, account_id: str):
        self.current_account_id = account_id
        self.is_authenticated = False

    def enter_pin(self, pin: str) -> bool:
        if not self.current_account_id:
            return False
        
        if self.bank_system.authenticate(self.current_account_id, pin):
            self.is_authenticated = True
            return True
        return False

    def check_balance(self) -> Optional[Decimal]:
        if not self.is_authenticated:
            return None
        return self.bank_system.get_balance(self.current_account_id)

    def withdraw(self, amount: Decimal) -> TransactionResult:
        if not self.is_authenticated:
            return TransactionResult.COMMUNICATION_ERROR
        if amount <= 0:
            return TransactionResult.COMMUNICATION_ERROR
            
        return self.bank_system.process_transaction(
            self.current_account_id, amount, TransactionType.WITHDRAWAL
        )

    def deposit(self, amount: Decimal) -> TransactionResult:
        if not self.is_authenticated:
            return TransactionResult.COMMUNICATION_ERROR
        
        return self.bank_system.process_transaction(
            self.current_account_id, amount, TransactionType.DEPOSIT
        )

    def eject_card(self):
        self.current_account_id = None
        self.is_authenticated = False

def simulate_atm_network():
    
    bank = CentralBankSystem()
    
    
    acc1 = Account("ACC123", "1234", Decimal("1000.00"))
    acc2 = Account("ACC456", "5678", Decimal("500.00"))
    bank.add_account(acc1)
    bank.add_account(acc2)

    
    atm = ATMController("ATM_SEATTLE_01", bank)

    
    print("--- Scenario 1: Withdrawal ---")
    atm.insert_card("ACC123")
    if atm.enter_pin("1234"):
        print(f"Auth Success. Balance: {atm.check_balance()}")
        res = atm.withdraw(Decimal("200.00"))
        print(f"Withdrawal Result: {res.value}")
        print(f"New Balance: {atm.check_balance()}")
    atm.eject_card()

    
    print("\n--- Scenario 2: Insufficient Funds ---")
    atm.insert_card("ACC456")
    atm.enter_pin("5678")
    res = atm.withdraw(Decimal("1000.00"))
    print(f"Withdrawal Result: {res.value}")
    atm.eject_card()

    
    print("\n--- Scenario 3: Deposit ---")
    atm.insert_card("ACC123")
    atm.enter_pin("1234")
    atm.deposit(Decimal("500.00"))
    print(f"New Balance after deposit: {atm.check_balance()}")
    atm.eject_card()

if __name__ == "__main__":
    simulate_atm_network()