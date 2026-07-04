import random
import datetime

class ATMController:
    def __init__(self, atm_network):
        self.atm_network = atm_network
        self.transactions = []

    def process_transaction(self, atm_id, transaction_type, amount):
        atm = self.atm_network.get_atm(atm_id)
        if atm is None:
            return False
        
        if transaction_type == "withdrawal":
            if atm.has_sufficient_cash(amount):
                atm.withdraw_cash(amount)
                transaction = {
                    "atm_id": atm_id,
                    "transaction_type": transaction_type,
                    "amount": amount,
                    "timestamp": datetime.datetime.now()
                }
                self.transactions.append(transaction)
                return True
            else:
                return False
        elif transaction_type == "deposit":
            atm.deposit_cash(amount)
            transaction = {
                "atm_id": atm_id,
                "transaction_type": transaction_type,
                "amount": amount,
                "timestamp": datetime.datetime.now()
            }
            self.transactions.append(transaction)
            return True
        else:
            return False

    def get_transaction_history(self, atm_id):
        return [t for t in self.transactions if t["atm_id"] == atm_id]

    def get_cash_levels(self):
        cash_levels = {}
        for atm in self.atm_network.get_atms():
            cash_levels[atm.id] = atm.cash_level
        return cash_levels

class ATMNetwork:
    def __init__(self):
        self.atms = []

    def add_atm(self, atm):
        self.atms.append(atm)

    def get_atm(self, atm_id):
        for atm in self.atms:
            if atm.id == atm_id:
                return atm
        return None

    def get_atms(self):
        return self.atms

class ATM:
    def __init__(self, id, cash_level):
        self.id = id
        self.cash_level = cash_level

    def withdraw_cash(self, amount):
        self.cash_level -= amount

    def deposit_cash(self, amount):
        self.cash_level += amount

    def has_sufficient_cash(self, amount):
        return self.cash_level >= amount


atm_network = ATMNetwork()
atm1 = ATM(1, 50000)
atm2 = ATM(2, 30000)
atm3 = ATM(3, 75000)

atm_network.add_atm(atm1)
atm_network.add_atm(atm2)
atm_network.add_atm(atm3)

controller = ATMController(atm_network)


controller.process_transaction(1, "withdrawal", 1000)
controller.process_transaction(2, "withdrawal", 2000)
controller.process_transaction(3, "deposit", 5000)


print(controller.get_transaction_history(1))
print(controller.get_transaction_history(2))
print(controller.get_transaction_history(3))


print(controller.get_cash_levels())