import unittest
from decimal import Decimal
from datetime import datetime

class BankCloudDatabase:
    
    def __init__(self):
        self._storage = {}

    def create_account(self, card_id, pin, initial_balance):
        self._storage[card_id] = {
            "pin": pin,
            "balance": Decimal(str(initial_balance)),
            "status": "ACTIVE",
            "transactions": []
        }

    def get_account_data(self, card_id):
        return self._storage.get(card_id)

    def update_account_balance(self, card_id, new_balance, transaction_type):
        if card_id in self._storage:
            self._storage[card_id]["balance"] = new_balance
            self._storage[card_id]["transactions"].append({
                "timestamp": datetime.now().isoformat(),
                "type": transaction_type,
                "amount": float(new_balance)
            })
            return True
        return False

class ATM:
    
    def __init__(self, atm_id, backend):
        self.atm_id = atm_id
        self.backend = backend
        self.session_card = None
        self.is_authenticated = False

    def insert_card(self, card_id):
        self.session_card = card_id
        self.is_authenticated = False
        return f"ATM {self.atm_id}: Card {card_id} accepted."

    def verify_pin(self, pin):
        account = self.backend.get_account_data(self.session_card)
        if account and account["pin"] == pin:
            self.is_authenticated = True
            return True
        return False

    def check_balance(self):
        if not self.is_authenticated:
            raise PermissionError("Authentication required.")
        account = self.backend.get_account_data(self.session_card)
        return account["balance"]

    def withdraw(self, amount):
        if not self.is_authenticated:
            raise PermissionError("Authentication required.")
        
        amount = Decimal(str(amount))
        account = self.backend.get_account_data(self.session_card)
        
        if account["balance"] >= amount:
            new_balance = account["balance"] - amount
            self.backend.update_account_balance(self.session_card, new_balance, "WITHDRAWAL")
            return new_balance
        else:
            raise ValueError("Insufficient funds.")

    def deposit(self, amount):
        if not self.is_authenticated:
            raise PermissionError("Authentication required.")
        
        amount = Decimal(str(amount))
        account = self.backend.get_account_data(self.session_card)
        new_balance = account["balance"] + amount
        self.backend.update_account_balance(self.session_card, new_balance, "DEPOSIT")
        return new_balance

    def end_session(self):
        self.session_card = None
        self.is_authenticated = False
        return "Session terminated."

class ATMNetworkController:
    
    def __init__(self):
        self.backend = BankCloudDatabase()
        self.atm_registry = {}

    def provision_atm(self, atm_id):
        new_atm = ATM(atm_id, self.backend)
        self.atm_registry[atm_id] = new_atm
        return new_atm

    def get_atm_instance(self, atm_id):
        return self.atm_registry.get(atm_id)

class TestATMController(unittest.TestCase):
    
    def setUp(self):
        self.controller = ATMNetworkController()
        self.controller.backend.create_account("12345", "9988", 1000.00)
        self.atm = self.controller.provision_atm("BRISTOL_01")

    def test_authentication_flow(self):
        self.atm.insert_card("12345")
        self.assertTrue(self.atm.verify_pin("9988"))
        self.assertFalse(self.atm.verify_pin("0000"))

    def test_withdrawal_logic(self):
        self.atm.insert_card("12345")
        self.atm.verify_pin("9988")
        self.atm.withdraw(200)
        self.assertEqual(self.atm.check_balance(), Decimal("800.00"))

    def test_insufficient_funds_error(self):
        self.atm.insert_card("12345")
        self.atm.verify_pin("9988")
        with self.assertRaises(ValueError):
            self.atm.withdraw(5000)

    def test_unauthorized_access(self):
        self.atm.insert_card("12345")
        with self.assertRaises(PermissionError):
            self.atm.check_balance()

if __name__ == "__main__":
    
    network = ATMNetworkController()
    
    
    network.backend.create_account("112233", "1234", 500.00)
    
    
    my_atm = network.provision_atm("LONDON_MALL_1")
    print(my_atm.insert_card("112233"))
    
    if my_atm.verify_pin("1234"):
        print(f"Initial Balance: £{my_atm.check_balance()}")
        my_atm.deposit(150.50)
        print(f"After Deposit: £{my_atm.check_balance()}")
        my_atm.withdraw(100.00)
        print(f"After Withdrawal: £{my_atm.check_balance()}")
        print(my_atm.end_session())
    else:
        print("Invalid PIN")

    
    print("\n--- Running System Unit Tests ---")
    unittest.main(argv=[''], exit=False)