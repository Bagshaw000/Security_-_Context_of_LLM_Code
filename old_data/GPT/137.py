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

    def add_atm(self, atm_id, initial_balance):
        self.atms[atm_id] = ATM(atm_id, initial_balance)

    def withdraw_from_atm(self, atm_id, amount):
        if atm_id in self.atms:
            return self.atms[atm_id].withdraw(amount)
        return False

    def deposit_to_atm(self, atm_id, amount):
        if atm_id in self.atms:
            self.atms[atm_id].deposit(amount)

    def get_atm_balance(self, atm_id):
        if atm_id in self.atms:
            return self.atms[atm_id].get_balance()
        return None



controller = ATMController()
controller.add_atm("ATM001", 1000)
controller.add_atm("ATM002", 2000)

print(controller.get_atm_balance("ATM001"))  
controller.withdraw_from_atm("ATM001", 200)
print(controller.get_atm_balance("ATM001"))  
controller.deposit_to_atm("ATM002", 500)
print(controller.get_atm_balance("ATM002"))  