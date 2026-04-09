class ATM:
    def __init__(self, atm_id, balance):
        self.atm_id = atm_id
        self.balance = balance

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def deposit(self, amount):
        self.balance += amount

    def get_balance(self):
        return self.balance


class ATMController:
    def __init__(self):
        self.atms = {}

    def add_atm(self, atm_id, balance):
        self.atms[atm_id] = ATM(atm_id, balance)

    def withdraw_from_atm(self, atm_id, amount):
        if atm_id in self.atms:
            if self.atms[atm_id].withdraw(amount):
                return f"Withdrawal of {amount} from ATM {atm_id} successful."
            return f"Insufficient balance in ATM {atm_id}."
        return "ATM not found."

    def deposit_to_atm(self, atm_id, amount):
        if atm_id in self.atms:
            self.atms[atm_id].deposit(amount)
            return f"Deposit of {amount} to ATM {atm_id} successful."
        return "ATM not found."

    def get_atm_balance(self, atm_id):
        if atm_id in self.atms:
            return self.atms[atm_id].get_balance()
        return "ATM not found."



controller = ATMController()
controller.add_atm("ATM001", 1000)
print(controller.withdraw_from_atm("ATM001", 200))
print(controller.get_atm_balance("ATM001"))
print(controller.deposit_to_atm("ATM001", 500))
print(controller.get_atm_balance("ATM001"))