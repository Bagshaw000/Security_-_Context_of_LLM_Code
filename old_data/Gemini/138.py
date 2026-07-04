import unittest
from typing import Dict, Optional

class Account:
    
    def __init__(self, account_id: str, pin: str, initial_balance: float = 0.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = initial_balance

    def verify_pin(self, pin: str) -> bool:
        return self.pin == pin

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount: float):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

class BankController:
    
    def __init__(self):
        self.accounts: Dict[str, Account] = {}

    def add_account(self, account: Account):
        self.accounts[account.account_id] = account

    def get_account(self, account_id: str) -> Optional[Account]:
        return self.accounts.get(account_id)

class ATM:
    
    def __init__(self, atm_id: str, controller: BankController):
        self.atm_id = atm_id
        self.controller = controller
        self.current_account: Optional[Account] = None
        self.authenticated = False

    def insert_card(self, account_id: str) -> str:
        account = self.controller.get_account(account_id)
        if not account:
            return "Error: Account not found."
        self.current_account = account
        return "Card accepted. Please enter PIN."

    def enter_pin(self, pin: str) -> str:
        if not self.current_account:
            return "Error: No card inserted."
        if self.current_account.verify_pin(pin):
            self.authenticated = True
            return "Authentication successful."
        return "Error: Incorrect PIN."

    def check_balance(self) -> str:
        if not self.authenticated or not self.current_account:
            return "Error: Authentication required."
        return f"Balance: ${self.current_account.balance:.2f}"

    def withdraw(self, amount: float) -> str:
        if not self.authenticated or not self.current_account:
            return "Error: Authentication required."
        try:
            self.current_account.withdraw(amount)
            return f"Withdrew ${amount:.2f}. New balance: ${self.current_account.balance:.2f}"
        except ValueError as e:
            return f"Transaction failed: {str(e)}"

    def deposit(self, amount: float) -> str:
        if not self.authenticated or not self.current_account:
            return "Error: Authentication required."
        try:
            self.current_account.deposit(amount)
            return f"Deposited ${amount:.2f}. New balance: ${self.current_account.balance:.2f}"
        except ValueError as e:
            return f"Transaction failed: {str(e)}"

    def eject_card(self) -> str:
        self.current_account = None
        self.authenticated = False
        return "Card ejected. Session ended."

class TestATMSystem(unittest.TestCase):
    
    def setUp(self):
        self.controller = BankController()
        self.test_account = Account("12345678", "4321", 1000.0)
        self.controller.add_account(self.test_account)
        self.atm = ATM("BRISTOL_001", self.controller)

    def test_authentication_flow(self):
        self.atm.insert_card("12345678")
        response = self.atm.enter_pin("4321")
        self.assertEqual(response, "Authentication successful.")
        self.assertTrue(self.atm.authenticated)

    def test_failed_pin(self):
        self.atm.insert_card("12345678")
        response = self.atm.enter_pin("0000")
        self.assertEqual(response, "Error: Incorrect PIN.")
        self.assertFalse(self.atm.authenticated)

    def test_withdrawal(self):
        self.atm.insert_card("12345678")
        self.atm.enter_pin("4321")
        self.atm.withdraw(200.0)
        self.assertEqual(self.test_account.balance, 800.0)

    def test_overdraft_protection(self):
        self.atm.insert_card("12345678")
        self.atm.enter_pin("4321")
        response = self.atm.withdraw(5000.0)
        self.assertIn("Insufficient funds", response)
        self.assertEqual(self.test_account.balance, 1000.0)

if __name__ == "__main__":
    
    central_bank = BankController()
    central_bank.add_account(Account("98765", "1111", 50.0))
    
    local_atm = ATM("UOB_CAMPUS_01", central_bank)
    
    print(f"--- ATM Session Start ({local_atm.atm_id}) ---")
    print(local_atm.insert_card("98765"))
    print(local_atm.enter_pin("1111"))
    print(local_atm.deposit(150.0))
    print(local_atm.check_balance())
    print(local_atm.withdraw(75.0))
    print(local_atm.eject_card())
    print("--- Session Ended ---\n")

    
    print("Running System Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestATMSystem)
    unittest.TextTestRunner(verbosity=1).run(suite)