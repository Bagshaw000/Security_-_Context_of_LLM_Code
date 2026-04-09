import hashlib
import uuid
from abc import ABC, abstractmethod
from decimal import Decimal
from threading import Lock
from typing import Dict, Optional, List
from datetime import datetime

class ATMSystemError(Exception):
    
    pass

class AuthenticationError(ATMSystemError):
    
    pass

class InsufficientFundsError(ATMSystemError):
    
    pass

class SecurityProvider:
    
    @staticmethod
    def hash_pin(pin: str, salt: str) -> str:
        return hashlib.sha256((pin + salt).encode()).hexdigest()

class Transaction:
    
    def __init__(self, transaction_type: str, amount: Decimal, account_id: str):
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        self.transaction_type = transaction_type
        self.amount = amount
        self.account_id = account_id

    def __repr__(self):
        return f"[{self.timestamp}] {self.transaction_type}: ${self.amount} (ID: {self.id})"

class Account:
    
    def __init__(self, account_id: str, pin: str, initial_balance: Decimal = Decimal('0.00')):
        self.account_id = account_id
        self.salt = uuid.uuid4().hex
        self.pin_hash = SecurityProvider.hash_pin(pin, self.salt)
        self.balance = initial_balance
        self.transactions: List[Transaction] = []
        self._lock = Lock()

    def verify_pin(self, pin: str) -> bool:
        return self.pin_hash == SecurityProvider.hash_pin(pin, self.salt)

    def deposit(self, amount: Decimal):
        with self._lock:
            if amount <= 0:
                raise ValueError("Deposit amount must be positive.")
            self.balance += amount
            self.transactions.append(Transaction("DEPOSIT", amount, self.account_id))

    def withdraw(self, amount: Decimal):
        with self._lock:
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive.")
            if self.balance < amount:
                raise InsufficientFundsError(f"Insufficient funds in account {self.account_id}")
            self.balance -= amount
            self.transactions.append(Transaction("WITHDRAWAL", amount, self.account_id))

class BankService(ABC):
    
    @abstractmethod
    def authenticate(self, account_id: str, pin: str) -> bool:
        pass

    @abstractmethod
    def get_balance(self, account_id: str) -> Decimal:
        pass

    @abstractmethod
    def process_transaction(self, account_id: str, amount: Decimal, tx_type: str):
        pass

class CoreBankSystem(BankService):
    
    def __init__(self, bank_name: str):
        self.bank_name = bank_name
        self.accounts: Dict[str, Account] = {}

    def add_account(self, account: Account):
        self.accounts[account.account_id] = account

    def authenticate(self, account_id: str, pin: str) -> bool:
        account = self.accounts.get(account_id)
        if account and account.verify_pin(pin):
            return True
        return False

    def get_balance(self, account_id: str) -> Decimal:
        if account_id not in self.accounts:
            raise ATMSystemError("Account not found.")
        return self.accounts[account_id].balance

    def process_transaction(self, account_id: str, amount: Decimal, tx_type: str):
        account = self.accounts.get(account_id)
        if not account:
            raise ATMSystemError("Account not found.")
        
        if tx_type == "WITHDRAW":
            account.withdraw(amount)
        elif tx_type == "DEPOSIT":
            account.deposit(amount)

class ATMController:
    
    def __init__(self):
        self.banks: Dict[str, BankService] = {}
        self._session_token: Optional[str] = None
        self._active_account: Optional[str] = None
        self._active_bank: Optional[str] = None

    def register_bank(self, bank_id: str, bank_service: BankService):
        self.banks[bank_id] = bank_service

    def insert_card(self, bank_id: str, account_id: str, pin: str):
        
        bank = self.banks.get(bank_id)
        if not bank:
            raise ATMSystemError("Unsupported bank.")
        
        if bank.authenticate(account_id, pin):
            self._active_account = account_id
            self._active_bank = bank_id
            self._session_token = uuid.uuid4().hex
            return True
        else:
            raise AuthenticationError("Invalid PIN or Account ID.")

    def check_balance(self) -> Decimal:
        self._validate_session()
        return self.banks[self._active_bank].get_balance(self._active_account)

    def withdraw_cash(self, amount: Decimal):
        self._validate_session()
        self.banks[self._active_bank].process_transaction(
            self._active_account, amount, "WITHDRAW"
        )

    def deposit_cash(self, amount: Decimal):
        self._validate_session()
        self.banks[self._active_bank].process_transaction(
            self._active_account, amount, "DEPOSIT"
        )

    def end_session(self):
        self._active_account = None
        self._active_bank = None
        self._session_token = None

    def _validate_session(self):
        if not self._session_token:
            raise AuthenticationError("No active session. Please insert card and enter PIN.")

class ATMHardwareInterface:
    
    def __init__(self, atm_id: str, controller: ATMController):
        self.atm_id = atm_id
        self.controller = controller

    def user_login(self, bank_id: str, account_id: str, pin: str):
        try:
            if self.controller.insert_card(bank_id, account_id, pin):
                print(f"ATM {self.atm_id}: Login successful.")
        except AuthenticationError as e:
            print(f"ATM {self.atm_id}: Login failed - {e}")

    def show_balance(self):
        try:
            balance = self.controller.check_balance()
            print(f"ATM {self.atm_id}: Current Balance is ${balance}")
        except ATMSystemError as e:
            print(f"ATM {self.atm_id}: Error - {e}")

    def withdraw(self, amount: float):
        try:
            self.controller.withdraw_cash(Decimal(str(amount)))
            print(f"ATM {self.atm_id}: Successfully withdrew ${amount}")
        except ATMSystemError as e:
            print(f"ATM {self.atm_id}: Withdrawal failed - {e}")

    def deposit(self, amount: float):
        try:
            self.controller.deposit_cash(Decimal(str(amount)))
            print(f"ATM {self.atm_id}: Successfully deposited ${amount}")
        except ATMSystemError as e:
            print(f"ATM {self.atm_id}: Deposit failed - {e}")

    def logout(self):
        self.controller.end_session()
        print(f"ATM {self.atm_id}: Session ended. Please take your card.")

if __name__ == "__main__":
    
    controller = ATMController()
    amazon_bank = CoreBankSystem("AmazonGlobalBank")
    
    
    test_acc_id = "AMZN-789-123"
    test_pin = "4321"
    amazon_bank.add_account(Account(test_acc_id, test_pin, Decimal('1500.00')))
    
    
    controller.register_bank("AMZN_CORE", amazon_bank)
    
    
    atm_unit_1 = ATMHardwareInterface("STATION_001", controller)
    
    
    atm_unit_1.user_login("AMZN_CORE", test_acc_id, test_pin)
    atm_unit_1.show_balance()
    atm_unit_1.withdraw(200.00)
    atm_unit_1.show_balance()
    atm_unit_1.deposit(50.00)
    atm_unit_1.show_balance()
    atm_unit_1.logout()