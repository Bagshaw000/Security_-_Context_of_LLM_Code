import uuid
from datetime import datetime
import unittest

class Account:
    
    def __init__(self, account_id, pin, initial_balance=0.0):
        self.account_id = account_id
        self.pin = pin
        self.balance = initial_balance
        self.transaction_history = []

    def add_transaction(self, transaction_type, amount):
        self.transaction_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': transaction_type,
            'amount': amount,
            'new_balance': self.balance
        })

class BankCentralServer:
    
    def __init__(self):
        
        self.accounts = {}

    def register_account(self, account):
        self.accounts[account.account_id] = account

    def authenticate_user(self, account_id, pin):
        account = self.accounts.get(account_id)
        if account and account.pin == pin:
            return True
        return False

    def get_account_balance(self, account_id):
        account = self.accounts.get(account_id)
        return account.balance if account else None

    def process_withdrawal(self, account_id, amount):
        account = self.accounts.get(account_id)
        if not account:
            return False, "Account not found."
        
        if account.balance >= amount:
            account.balance -= amount
            account.add_transaction("WITHDRAWAL", amount)
            return True, "Transaction successful."
        else:
            return False, "Insufficient funds."

    def process_deposit(self, account_id, amount):
        account = self.accounts.get(account_id)
        if not account:
            return False, "Account not found."
        
        account.balance += amount
        account.add_transaction("DEPOSIT", amount)
        return True, "Deposit successful."

class ATM:
    
    def __init__(self, atm_id, central_server):
        self.atm_id = atm_id
        self.central_server = central_server
        self.session_account_id = None
        self.is_authenticated = False

    def insert_card(self, account_id):
        self.session_account_id = account_id
        print(f"[ATM {self.atm_id}] Card detected for account: {account_id}")

    def enter_pin(self, pin):
        if not self.session_account_id:
            return "Please insert card first."
        
        if self.central_server.authenticate_user(self.session_account_id, pin):
            self.is_authenticated = True
            return "Authenticated successfully."
        else:
            return "Invalid PIN."

    def check_balance(self):
        if not self.is_authenticated:
            return "Authentication required."
        balance = self.central_server.get_account_balance(self.session_account_id)
        return f"Current Balance: ${balance:.2f}"

    def withdraw_cash(self, amount):
        if not self.is_authenticated:
            return "Authentication required."
        
        success, message = self.central_server.process_withdrawal(self.session_account_id, amount)
        return message

    def deposit_cash(self, amount):
        if not self.is_authenticated:
            return "Authentication required."
        
        success, message = self.central_server.process_deposit(self.session_account_id, amount)
        return message

    def eject_card(self):
        self.session_account_id = None
        self.is_authenticated = False
        return "Card ejected. Session ended."

class TestATMSystem(unittest.TestCase):
    
    def setUp(self):
        self.server = BankCentralServer()
        self.test_acc = Account("12345678", "4433", 1000.0)
        self.server.register_account(self.test_acc)
        self.atm = ATM("BRISTOL_001", self.server)

    def test_successful_flow(self):
        self.atm.insert_card("12345678")
        auth_status = self.atm.enter_pin("4433")
        self.assertEqual(auth_status, "Authenticated successfully.")
        
        withdrawal_msg = self.atm.withdraw_cash(200.0)
        self.assertEqual(withdrawal_msg, "Transaction successful.")
        
        balance_msg = self.atm.check_balance()
        self.assertEqual(balance_msg, "Current Balance: $800.00")

    def test_failed_auth(self):
        self.atm.insert_card("12345678")
        auth_status = self.atm.enter_pin("0000")
        self.assertEqual(auth_status, "Invalid PIN.")
        self.assertEqual(self.atm.check_balance(), "Authentication required.")

    def test_overdraft_protection(self):
        self.atm.insert_card("12345678")
        self.atm.enter_pin("4433")
        msg = self.atm.withdraw_cash(5000.0)
        self.assertEqual(msg, "Insufficient funds.")

if __name__ == "__main__":
    
    server = BankCentralServer()
    john_account = Account("98765432", "1122", 500.0)
    server.register_account(john_account)
    
    local_atm = ATM("LONDON_STATION_1", server)
    local_atm.insert_card("98765432")
    print(local_atm.enter_pin("1122"))
    print(local_atm.withdraw_cash(100.0))
    print(local_atm.check_balance())
    print(local_atm.eject_card())

    
    print("\nRunning System Unit Tests...")
    unittest.main(argv=[''], exit=False)