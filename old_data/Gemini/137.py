import unittest
from typing import Dict, Any, Optional

class BankCentralSystem:
    
    def __init__(self):
        
        self._accounts = {
            "ACC1001": {"pin": "4321", "balance": 1500.00, "status": "active"},
            "ACC1002": {"pin": "8888", "balance": 50.00, "status": "active"},
            "ACC1003": {"pin": "1234", "balance": 10000.00, "status": "locked"}
        }

    def verify_pin(self, account_id: str, pin: str) -> bool:
        account = self._accounts.get(account_id)
        if account and account["status"] == "active":
            return account["pin"] == pin
        return False

    def get_account_balance(self, account_id: str) -> float:
        if account_id not in self._accounts:
            raise ValueError("Account not found")
        return self._accounts[account_id]["balance"]

    def process_transaction(self, account_id: str, amount: float) -> bool:
        
        if account_id not in self._accounts:
            return False
            
        current_balance = self._accounts[account_id]["balance"]
        if current_balance + amount < 0:
            return False
        
        self._accounts[account_id]["balance"] += amount
        return True

class ATMUnit:
    
    def __init__(self, terminal_id: str, bank_system: BankCentralSystem):
        self.terminal_id = terminal_id
        self.bank_system = bank_system
        self.session_account_id: Optional[str] = None

    def authenticate_user(self, account_id: str, pin: str) -> bool:
        if self.bank_system.verify_pin(account_id, pin):
            self.session_account_id = account_id
            return True
        return False

    def check_balance(self) -> float:
        if not self.session_account_id:
            raise PermissionError("No active session. Please authenticate.")
        return self.bank_system.get_account_balance(self.session_account_id)

    def withdraw_cash(self, amount: float) -> bool:
        if not self.session_account_id:
            raise PermissionError("No active session. Please authenticate.")
        if amount <= 0:
            return False
        return self.bank_system.process_transaction(self.session_account_id, -amount)

    def deposit_cash(self, amount: float) -> bool:
        if not self.session_account_id:
            raise PermissionError("No active session. Please authenticate.")
        if amount <= 0:
            return False
        return self.bank_system.process_transaction(self.session_account_id, amount)

    def end_session(self):
        self.session_account_id = None

class ATMNetworkController:
    
    def __init__(self):
        self.central_bank = BankCentralSystem()
        self.active_terminals: Dict[str, ATMUnit] = {}

    def deploy_atm(self, terminal_id: str) -> ATMUnit:
        
        new_atm = ATMUnit(terminal_id, self.central_bank)
        self.active_terminals[terminal_id] = new_atm
        return new_atm

    def get_terminal_status(self, terminal_id: str) -> str:
        if terminal_id in self.active_terminals:
            return "Online"
        return "Offline"

class TestATMController(unittest.TestCase):
    
    def setUp(self):
        self.controller = ATMNetworkController()
        self.atm = self.controller.deploy_atm("BRISTOL-001")

    def test_authentication_success(self):
        self.assertTrue(self.atm.authenticate_user("ACC1001", "4321"))

    def test_authentication_failure(self):
        self.assertFalse(self.atm.authenticate_user("ACC1001", "0000"))

    def test_withdrawal_logic(self):
        self.atm.authenticate_user("ACC1001", "4321")
        initial_balance = self.atm.check_balance()
        withdrawal_amount = 200.0
        success = self.atm.withdraw_cash(withdrawal_amount)
        self.assertTrue(success)
        self.assertEqual(self.atm.check_balance(), initial_balance - withdrawal_amount)

    def test_insufficient_funds(self):
        self.atm.authenticate_user("ACC1002", "8888")
        
        success = self.atm.withdraw_cash(100.0)
        self.assertFalse(success)

    def test_locked_account(self):
        
        self.assertFalse(self.atm.authenticate_user("ACC1003", "1234"))

    def test_session_security(self):
        self.atm.authenticate_user("ACC1001", "4321")
        self.atm.end_session()
        with self.assertRaises(PermissionError):
            self.atm.check_balance()

if __name__ == "__main__":
    
    unittest.main(exit=False)