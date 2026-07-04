class ATM:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

class ATMController:
    def __init__(self):
        self.atms = {}

    def add_atm(self, atm):
        self.atms[atm.name] = atm

    def get_atm_balance(self, atm_name):
        return self.atms[atm_name].balance

    def deposit(self, atm_name, amount):
        if atm_name in self.atms:
            self.atms[atm_name].balance += amount
        else:
            print("ATM not found.")

    def withdraw(self, atm_name, amount):
        if atm_name in self.atms and self.atms[atm_name].balance >= amount:
            self.atms[atm_name].balance -= amount
        else:
            print("Insufficient funds or ATM not found.")