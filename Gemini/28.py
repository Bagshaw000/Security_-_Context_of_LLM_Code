import logging
import uuid
import threading
from decimal import Decimal
from typing import Dict, Optional
from datetime import datetime


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ATMError(Exception):
    
    pass

class AuthenticationError(ATMError):
    
    pass

class InsufficientFundsError(ATMError):
    
    pass

class Account:
    
    def __init__(self, account_id: str, pin: str, initial_balance: Decimal = Decimal('0.00')):
        self.account_id = account_id
        self.__pin = pin  
        self.balance = initial_balance
        self.lock = threading.Lock()

    def verify_pin(self, input_pin: str) -> bool:
        return self.__pin == input_pin

    def deposit(self, amount: Decimal):
        with self.lock:
            self.balance += amount

    def withdraw(self, amount: Decimal):
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
            else:
                raise InsufficientFundsError("Insufficient funds in account.")

class BankBackend:
    
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self._load_mock_data()

    def _load_mock_data(self):
        
        self.accounts["123456789"] = Account("123456789", "1234", Decimal("1500.00"))
        self.accounts["987654321"] = Account("987654321", "4321", Decimal("500.00"))

    def get_account(self, account_id: str) -> Optional[Account]:
        return self.accounts.get(account_id)

class ATMController:
    
    def __init__(self, backend: BankBackend):
        self.backend = backend
        self.active_sessions: Dict[str, str] = {} 

    def authenticate(self, account_id: str, pin: str) -> str:
        
        account = self.backend.get_account(account_id)
        if account and account.verify_pin(pin):
            session_id = str(uuid.uuid4())
            self.active_sessions[session_id] = account_id
            logging.info(f"Account {account_id} authenticated. Session: {session_id}")
            return session_id
        raise AuthenticationError("Invalid Account ID or PIN.")

    def get_balance(self, session_id: str) -> Decimal:
        account_id = self._validate_session(session_id)
        account = self.backend.get_account(account_id)
        return account.balance

    def withdraw(self, session_id: str, amount: Decimal) -> Decimal:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        
        account_id = self._validate_session(session_id)
        account = self.backend.get_account(account_id)
        
        account.withdraw(amount)
        logging.info(f"Session {session_id}: Withdrew {amount}. New Balance: {account.balance}")
        return account.balance

    def deposit(self, session_id: str, amount: Decimal) -> Decimal:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
            
        account_id = self._validate_session(session_id)
        account = self.backend.get_account(account_id)
        
        account.deposit(amount)
        logging.info(f"Session {session_id}: Deposited {amount}. New Balance: {account.balance}")
        return account.balance

    def logout(self, session_id: str):
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logging.info(f"Session {session_id} terminated.")

    def _validate_session(self, session_id: str) -> str:
        if session_id not in self.active_sessions:
            raise AuthenticationError("Session invalid or expired.")
        return self.active_sessions[session_id]

class ATMTerminal:
    
    def __init__(self, terminal_id: str, controller: ATMController):
        self.terminal_id = terminal_id
        self.controller = controller
        self.current_session: Optional[str] = None

    def insert_card_and_pin(self, account_id: str, pin: str):
        try:
            self.current_session = self.controller.authenticate(account_id, pin)
            print(f"[{self.terminal_id}] Login Successful.")
        except AuthenticationError as e:
            print(f"[{self.terminal_id}] Login Failed: {e}")

    def check_balance(self):
        if not self.current_session:
            print("Please login first.")
            return
        balance = self.controller.get_balance(self.current_session)
        print(f"[{self.terminal_id}] Current Balance: ${balance}")

    def withdraw_cash(self, amount: float):
        if not self.current_session:
            print("Please login first.")
            return
        try:
            new_balance = self.controller.withdraw(self.current_session, Decimal(str(amount)))
            print(f"[{self.terminal_id}] Please take your cash. Remaining: ${new_balance}")
        except ATMError as e:
            print(f"[{self.terminal_id}] Transaction Failed: {e}")

    def deposit_cash(self, amount: float):
        if not self.current_session:
            print("Please login first.")
            return
        new_balance = self.controller.deposit(self.current_session, Decimal(str(amount)))
        print(f"[{self.terminal_id}] Deposit accepted. New Balance: ${new_balance}")

    def exit(self):
        if self.current_session:
            self.controller.logout(self.current_session)
            self.current_session = None
            print(f"[{self.terminal_id}] Session closed. Thank you.")


if __name__ == "__main__":
    
    central_bank = BankBackend()

    
    atm_network_controller = ATMController(central_bank)

    
    atm_unit_101 = ATMTerminal("ATM-NYC-001", atm_network_controller)
    atm_unit_102 = ATMTerminal("ATM-SEA-054", atm_network_controller)

    
    print("--- NYC ATM Transaction ---")
    atm_unit_101.insert_card_and_pin("123456789", "1234")
    atm_unit_101.check_balance()
    atm_unit_101.withdraw_cash(200.00)
    atm_unit_101.exit()

    print("\n--- Seattle ATM Transaction ---")
    
    atm_unit_102.insert_card_and_pin("987654321", "4321")
    atm_unit_102.deposit_cash(1000.00)
    atm_unit_102.withdraw_cash(2000.00) 
    atm_unit_102.exit()

    
    print("\n--- Security Check ---")
    atm_unit_101.insert_card_and_pin("123456789", "wrong_pin")
    atm_unit_101.check_balance()