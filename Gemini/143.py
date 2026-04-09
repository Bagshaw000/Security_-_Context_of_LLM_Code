import hashlib
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

class TransactionStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"

class ATMException(Exception):
    
    pass

class InsufficientFundsException(ATMException):
    pass

class AuthenticationException(ATMException):
    pass

class DeviceSecurityException(ATMException):
    pass

class Account:
    
    def __init__(self, account_id: str, pin_hash: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.pin_hash = pin_hash
        self.balance = initial_balance
        self.status = "ACTIVE"

    def verify_pin(self, pin: str) -> bool:
        return hashlib.sha256(pin.encode()).hexdigest() == self.pin_hash

class BankServer:
    
    def __init__(self):
        self._accounts: Dict[str, Account] = {}
        self._registered_atms: Dict[str, Dict[str, Any]] = {}
        self._transaction_history: List[Dict[str, Any]] = []

    def register_atm_device(self, atm_id: str, metadata: Dict[str, Any]):
        
        self._registered_atms[atm_id] = {
            "metadata": metadata,
            "status": "ONLINE",
            "provisioned_at": datetime.utcnow()
        }

    def add_account(self, account: Account):
        self._accounts[account.account_id] = account

    def authorize_request(self, atm_id: str, account_id: str, pin: str) -> bool:
        
        if atm_id not in self._registered_atms:
            raise DeviceSecurityException(f"Device {atm_id} is unauthorized.")
        
        account = self._accounts.get(account_id)
        if not account or not account.verify_pin(pin):
            raise AuthenticationException("Invalid account identifier or security code.")
        
        return True

    def execute_transaction(self, account_id: str, amount: float) -> TransactionStatus:
        
        account = self._accounts.get(account_id)
        if not account:
            return TransactionStatus.FAILED

        if account.balance + amount < 0:
            raise InsufficientFundsException("Account balance insufficient for request.")

        account.balance += amount
        self._transaction_history.append({
            "id": str(uuid.uuid4()),
            "account_id": account_id,
            "delta": amount,
            "timestamp": datetime.utcnow()
        })
        return TransactionStatus.COMPLETED

    def fetch_balance(self, account_id: str) -> float:
        return self._accounts[account_id].balance

class ATMController:
    
    def __init__(self, atm_id: str, server: BankServer):
        self.atm_id = atm_id
        self.server = server
        self._session_account_id: Optional[str] = None
        self._authenticated: bool = False

    def insert_card(self, account_id: str):
        self._session_account_id = account_id
        print(f"ATM {self.atm_id}: Card detected for {account_id}")

    def input_pin(self, pin: str) -> bool:
        if not self._session_account_id:
            return False
        
        try:
            self._authenticated = self.server.authorize_request(
                self.atm_id, self._session_account_id, pin
            )
            return True
        except ATMException as e:
            print(f"Security Alert: {e}")
            self.eject_card()
            return False

    def get_balance(self) -> float:
        self._validate_session()
        return self.server.fetch_balance(self._session_account_id)

    def withdraw(self, amount: float):
        self._validate_session()
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        try:
            status = self.server.execute_transaction(self._session_account_id, -amount)
            if status == TransactionStatus.COMPLETED:
                print(f"Dispensing {amount}...")
        except InsufficientFundsException:
            print("Error: Insufficient funds in account.")

    def deposit(self, amount: float):
        self._validate_session()
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        status = self.server.execute_transaction(self._session_account_id, amount)
        if status == TransactionStatus.COMPLETED:
            print(f"Successfully deposited {amount}.")

    def eject_card(self):
        self._session_account_id = None
        self._authenticated = False
        print("Card ejected. Clear session data.")

    def _validate_session(self):
        if not self._authenticated:
            raise AuthenticationException("Active session required for this operation.")

if __name__ == "__main__":
    
    central_server = BankServer()
    
    
    secure_pin = "5566"
    hashed_pin = hashlib.sha256(secure_pin.encode()).hexdigest()
    user_acc = Account("USER_ID_9901", hashed_pin, 2500.0)
    central_server.add_account(user_acc)
    
    
    my_atm_id = "SEA_HUB_01"
    central_server.register_atm_device(my_atm_id, {"location": "Seattle", "model": "NCR-6682"})

    
    controller = ATMController(my_atm_id, central_server)
    
    
    controller.insert_card("USER_ID_9901")
    if controller.input_pin("5566"):
        print(f"Current Balance: ${controller.get_balance()}")
        controller.withdraw(400.0)
        controller.deposit(150.0)
        print(f"Updated Balance: ${controller.get_balance()}")
        controller.eject_card()
    else:
        print("Access Denied.")