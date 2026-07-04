import random

class ATMController:
    def __init__(self, num_atms):
        self.atms = [ATM(i) for i in range(num_atms)]
        self.transactions = []

    def process_transaction(self, transaction):
        atm = self.get_available_atm()
        if atm:
            atm.process_transaction(transaction)
            self.transactions.append(transaction)
        else:
            print(f"No available ATM to process transaction: {transaction}")

    def get_available_atm(self):
        for atm in self.atms:
            if atm.is_available():
                return atm
        return None

class ATM:
    def __init__(self, id):
        self.id = id
        self.available = True
        self.cash_level = 10000

    def is_available(self):
        return self.available

    def process_transaction(self, transaction):
        self.available = False
        if self.cash_level >= transaction.amount:
            self.cash_level -= transaction.amount
            print(f"ATM {self.id} processed transaction: {transaction}")
        else:
            print(f"ATM {self.id} does not have enough cash to process transaction: {transaction}")
        self.available = True

class Transaction:
    def __init__(self, id, amount):
        self.id = id
        self.amount = amount

    def __str__(self):
        return f"Transaction ID: {self.id}, Amount: {self.amount}"


controller = ATMController(5)

for i in range(10):
    transaction = Transaction(i, random.randint(100, 1000))
    controller.process_transaction(transaction)