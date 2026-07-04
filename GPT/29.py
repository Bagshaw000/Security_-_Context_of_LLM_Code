class ATM:
    def __init__(self, atm_id, balance):
        self.atm_id = atm_id
        self.balance = balance

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return amount
        else:
            return "Insufficient funds"

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def get_balance(self):
        return self.balance


class ATMNetwork:
    def __init__(self):
        self.atms = {}

    def add_atm(self, atm_id, balance):
        self.atms[atm_id] = ATM(atm_id, balance)

    def withdraw_from_atm(self, atm_id, amount):
        if atm_id in self.atms:
            return self.atms[atm_id].withdraw(amount)
        else:
            return "ATM not found"

    def deposit_to_atm(self, atm_id, amount):
        if atm_id in self.atms:
            return self.atms[atm_id].deposit(amount)
        else:
            return "ATM not found"

    def get_atm_balance(self, atm_id):
        if atm_id in self.atms:
            return self.atms[atm_id].get_balance()
        else:
            return "ATM not found"



network = ATMNetwork()
network.add_atm("ATM001", 1000)
network.add_atm("ATM002", 2000)

print(network.withdraw_from_atm("ATM001", 150))  
print(network.get_atm_balance("ATM001"))          
print(network.deposit_to_atm("ATM002", 500))      
print(network.get_atm_balance("ATM002"))          