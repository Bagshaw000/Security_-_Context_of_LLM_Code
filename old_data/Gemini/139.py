import uuid
import logging
from datetime import datetime
from typing import Dict, Optional, List


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ATMController")

class InsufficientFundsError(Exception):
    pass

class InvalidPinError(Exception):
    pass

class AccountNotFoundError(Exception):
    pass

class Account:
    def __init__(self, account_id: str, pin: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = initial_balance

    def verify_pin(self, pin: str) -> bool:
        return self.pin == pin

    def update_balance(self, amount: float):
        if self.balance + amount < 0:
            raise InsufficientFundsError("Insufficient funds in account.")
        self.balance += amount

class BankDatabase:
    
    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def add_account(self, account: Account):
        self.accounts[account.account_id] = account

    def get_account(self, account_id: str) -> Optional[Account]:
        return self.accounts.get(account_id)

class ATM:
    def __init__(self, atm_id: str, current_cash: float):
        self.atm_id = atm_id
        self.current_cash = current_cash
        self.is_active = True

    def dispense_cash(self, amount: float):
        if amount > self.current_cash:
            raise ValueError("ATM has insufficient physical cash.")
        self.current_cash -= amount

class ATMController:
    
    def __init__(self, database: BankDatabase):
        self.database = database
        self.atms: Dict[str, ATM] = {}
        self.active_sessions: Dict[str, str] = {} 

    def register_atm(self, atm: ATM):
        self.atms[atm.atm_id] = atm
        logger.info(f"ATM {atm.atm_id} registered and online.")

    def authenticate_user(self, atm_id: str, account_id: str, pin: str) -> bool:
        account = self.database.get_account(account_id)
        if not account:
            logger.warning(f"Failed login attempt: Account {account_id} not found.")
            return False
        
        if account.verify_pin(pin):
            self.active_sessions[atm_id] = account_id
            logger.info(f"User {account_id} authenticated at ATM {atm_id}.")
            return True
        
        logger.warning(f"Failed login attempt: Incorrect PIN for account {account_id}.")
        return False

    def get_balance(self, atm_id: str) -> float:
        account_id = self.active_sessions.get(atm_id)
        if not account_id:
            raise PermissionError("No active session.")
        
        account = self.database.get_account(account_id)
        return account.balance

    def withdraw(self, atm_id: str, amount: float) -> bool:
        account_id = self.active_sessions.get(atm_id)
        if not account_id:
            raise PermissionError("No active session.")

        atm = self.atms.get(atm_id)
        account = self.database.get_account(account_id)

        try:
            if amount > atm.current_cash:
                logger.error(f"ATM {atm_id} failure: Insufficient physical cash.")
                return False

            account.update_balance(-amount)
            atm.dispense_cash(amount)
            
            logger.info(f"Transaction Success: {account_id} withdrew {amount} from ATM {atm_id}.")
            return True
        except InsufficientFundsError as e:
            logger.error(f"Transaction Denied: {str(e)}")
            return False

    def logout(self, atm_id: str):
        if atm_id in self.active_sessions:
            del self.active_sessions[atm_id]
            logger.info(f"Session closed for ATM {atm_id}.")

import unittest

class TestATMSystem(unittest.TestCase):
    def setUp(self):
        self.db = BankDatabase()
        self.db.add_account(Account("12345", "1111", 1000.0))
        self.controller = ATMController(self.db)
        self.atm1 = ATM("ATM_BRISTOL_01", 5000.0)
        self.controller.register_atm(self.atm1)

    def test_successful_withdrawal(self):
        self.controller.authenticate_user("ATM_BRISTOL_01", "12345", "1111")
        success = self.controller.withdraw("ATM_BRISTOL_01", 200.0)
        self.assertTrue(success)
        self.assertEqual(self.db.get_account("12345").balance, 800.0)
        self.assertEqual(self.atm1.current_cash, 4800.0)

    def test_invalid_pin(self):
        authenticated = self.controller.authenticate_user("ATM_BRISTOL_01", "12345", "9999")
        self.assertFalse(authenticated)

    def test_insufficient_funds(self):
        self.controller.authenticate_user("ATM_BRISTOL_01", "12345", "1111")
        success = self.controller.withdraw("ATM_BRISTOL_01", 2000.0)
        self.assertFalse(success)

if __name__ == "__main__":
    
    db = BankDatabase()
    db.add_account(Account("user_a", "4321", 500.0))
    
    ctrl = ATMController(db)
    my_atm = ATM("ATM_001", 10000.0)
    ctrl.register_atm(my_atm)
    
    if ctrl.authenticate_user("ATM_001", "user_a", "4321"):
        print(f"Current Balance: {ctrl.get_balance('ATM_001')}")
        ctrl.withdraw("ATM_001", 100.0)
        print(f"New Balance: {ctrl.get_balance('ATM_001')}")
        ctrl.logout("ATM_001")

    
    print("\nRunning unit tests...")
    unittest.main(exit=False)