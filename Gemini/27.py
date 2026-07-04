import unittest

class BankService:
    
    def __init__(self):
        
        self.accounts = {
            "acc_8821": {"pin": "4321", "balance": 2500.50},
            "acc_4432": {"pin": "9876", "balance": 120.00},
            "acc_1001": {"pin": "0000", "balance": 10000.00}
        }

    def verify_pin(self, account_id, pin):
        account = self.accounts.get(account_id)
        if account and account["pin"] == pin:
            return True
        return False

    def get_balance(self, account_id):
        return self.accounts.get(account_id, {}).get("balance", 0.0)

    def update_balance(self, account_id, amount):
        if account_id in self.accounts:
            self.accounts[account_id]["balance"] += amount
            return True
        return False

class ATMUnit:
    
    def __init__(self, atm_id, initial_cash):
        self.atm_id = atm_id
        self.cash_on_hand = initial_cash

    def has_sufficient_cash(self, amount):
        return self.cash_on_hand >= amount

    def dispense(self, amount):
        if self.has_sufficient_cash(amount):
            self.cash_on_hand -= amount
            return True
        return False

class ATMController:
    
    def __init__(self, bank_service):
        self.bank_service = bank_service
        self.network = {}
        self.active_account = None
        self.is_authenticated = False

    def register_atm(self, atm_unit):
        self.network[atm_unit.atm_id] = atm_unit

    def insert_card(self, account_id):
        self.active_account = account_id
        self.is_authenticated = False

    def enter_pin(self, pin):
        if not self.active_account:
            return "Error: No card inserted."
        
        if self.bank_service.verify_pin(self.active_account, pin):
            self.is_authenticated = True
            return "Success: Authenticated."
        return "Error: Invalid PIN."

    def check_balance(self):
        if not self.is_authenticated:
            return "Error: Authentication required."
        balance = self.bank_service.get_balance(self.active_account)
        return f"Balance: ${balance:.2f}"

    def withdraw(self, atm_id, amount):
        if not self.is_authenticated:
            return "Error: Authentication required."
        
        atm = self.network.get(atm_id)
        if not atm:
            return "Error: ATM unit not found in network."

        if not atm.has_sufficient_cash(amount):
            return "Error: ATM has insufficient cash reserves."

        current_balance = self.bank_service.get_balance(self.active_account)
        if amount > current_balance:
            return "Error: Insufficient account funds."

        
        if self.bank_service.update_balance(self.active_account, -amount):
            atm.dispense(amount)
            return f"Success: Please take your ${amount:.2f}."
        
        return "Error: Transaction failed at bank level."

    def eject_card(self):
        self.active_account = None
        self.is_authenticated = False

class TestATMSystem(unittest.TestCase):
    
    def setUp(self):
        self.bank = BankService()
        self.controller = ATMController(self.bank)
        self.atm = ATMUnit("BRISTOL_01", 5000.0)
        self.controller.register_atm(self.atm)

    def test_successful_flow(self):
        self.controller.insert_card("acc_8821")
        auth_result = self.controller.enter_pin("4321")
        self.assertEqual(auth_result, "Success: Authenticated.")
        
        balance_msg = self.controller.check_balance()
        self.assertEqual(balance_msg, "Balance: $2500.50")
        
        withdraw_msg = self.controller.withdraw("BRISTOL_01", 500.0)
        self.assertIn("Success", withdraw_msg)
        self.assertEqual(self.bank.get_balance("acc_8821"), 2000.50)
        self.assertEqual(self.atm.cash_on_hand, 4500.0)

    def test_failed_auth(self):
        self.controller.insert_card("acc_8821")
        result = self.controller.enter_pin("wrong_pin")
        self.assertEqual(result, "Error: Invalid PIN.")
        self.assertFalse(self.controller.is_authenticated)

    def test_insufficient_atm_cash(self):
        self.controller.insert_card("acc_1001")
        self.controller.enter_pin("0000")
        
        result = self.controller.withdraw("BRISTOL_01", 6000.0)
        self.assertEqual(result, "Error: ATM has insufficient cash reserves.")

if __name__ == "__main__":
    
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestATMSystem)
    runner.run(suite)

    
    bank_svc = BankService()
    controller = ATMController(bank_svc)
    local_atm = ATMUnit("STATION_RD_01", 2000.0)
    controller.register_atm(local_atm)

    print("--- ATM Session Started ---")
    controller.insert_card("acc_4432")
    print(controller.enter_pin("9876"))
    print(controller.check_balance())
    print(controller.withdraw("STATION_RD_01", 50.0))
    print(controller.check_balance())
    controller.eject_card()
    print("--- Session Ended ---")