import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Dict, Optional, List
from threading import Lock

class ATMSystemError(Exception):
    
    pass

class InsufficientFundsError(ATMSystemError):
    
    pass

class AuthenticationError(ATMSystemError):
    
    pass

class Account:
    
    def __init__(self, account_id: str, pin_hash: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.pin_hash = pin_hash
        self.balance = initial_balance
        self._lock = Lock()

    def verify_pin(self, pin: str) -> bool:
        
        return self.pin_hash == pin

    def get_balance(self) -> float:
        with self._lock:
            return self.balance

    def update_balance(self, amount: float):
        with self._lock:
            if self.balance + amount < 0:
                raise InsufficientFundsError("Transaction declined: Insufficient funds.")
            self.balance += amount

class Transaction(ABC):
    
    def __init__(self, amount: float):
        self.transaction_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow()
        self.amount = amount

    @abstractmethod
    def execute(self, account: Account):
        pass

class Withdrawal(Transaction):
    def execute(self, account: Account):
        account.update_balance(-self.amount)

class Deposit(Transaction):
    def execute(self, account: Account):
        account.update_balance(self.amount)

class CentralBankController:
    
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CentralBankController, cls).__new__(cls)
                cls._instance._accounts: Dict[str, Account] = {}
                cls._instance._active_sessions: Dict[str, str] = {}
        return cls._instance

    def register_account(self, account_id: str, pin: str, balance: float):
        self._accounts[account_id] = Account(account_id, pin, balance)

    def authenticate(self, account_id: str, pin: str) -> str:
        
        account = self._accounts.get(account_id)
        if account and account.verify_pin(pin):
            session_token = f"sess_{uuid.uuid4().hex}"
            self._active_sessions[session_token] = account_id
            return session_token
        raise AuthenticationError("Invalid account ID or PIN.")

    def authorize_and_execute(self, session_token: str, transaction: Transaction):
        
        account_id = self._active_sessions.get(session_token)
        if not account_id:
            raise AuthenticationError("Session expired or invalid.")
        
        account = self._accounts.get(account_id)
        transaction.execute(account)

    def query_balance(self, session_token: str) -> float:
        account_id = self._active_sessions.get(session_token)
        if not account_id:
            raise AuthenticationError("Session expired or invalid.")
        return self._accounts[account_id].get_balance()

    def terminate_session(self, session_token: str):
        self._active_sessions.pop(session_token, None)

class ATMController:
    
    def __init__(self, atm_id: str, bank_controller: CentralBankController):
        self.atm_id = atm_id
        self.bank_controller = bank_controller
        self._inserted_account_id: Optional[str] = None
        self._session_token: Optional[str] = None

    def insert_card(self, account_id: str):
        self._inserted_account_id = account_id

    def authenticate_user(self, pin: str) -> bool:
        if not self._inserted_account_id:
            return False
        try:
            self._session_token = self.bank_controller.authenticate(self._inserted_account_id, pin)
            return True
        except AuthenticationError:
            return False

    def check_balance(self) -> float:
        if not self._session_token:
            raise AuthenticationError("No active session.")
        return self.bank_controller.query_balance(self._session_token)

    def withdraw_cash(self, amount: float):
        if not self._session_token:
            raise AuthenticationError("No active session.")
        tx = Withdrawal(amount)
        self.bank_controller.authorize_and_execute(self._session_token, tx)

    def deposit_funds(self, amount: float):
        if not self._session_token:
            raise AuthenticationError("No active session.")
        tx = Deposit(amount)
        self.bank_controller.authorize_and_execute(self._session_token, tx)

    def close_session(self):
        if self._session_token:
            self.bank_controller.terminate_session(self._session_token)
        self._inserted_account_id = None
        self._session_token = None

if __name__ == "__main__":
    
    bank_service = CentralBankController()
    bank_service.register_account("ACC-7788", "1234", 2500.0)

    
    atm_unit = ATMController("SEA-TX-01", bank_service)
    
    
    atm_unit.insert_card("ACC-7788")
    
    
    if atm_unit.authenticate_user("1234"):
        print(f"Auth Success. Current Balance: ${atm_unit.check_balance():.2f}")
        
        try:
            
            atm_unit.withdraw_cash(500.0)
            print("Withdrawal successful.")
            
            
            atm_unit.deposit_funds(150.0)
            print("Deposit successful.")
            
            print(f"New Balance: ${atm_unit.check_balance():.2f}")
        except ATMSystemError as e:
            print(f"Transaction failed: {e}")
        finally:
            
            atm_unit.close_session()
            print("Session closed. Card ejected.")
    else:
        print("Authentication failed. Please try again.")