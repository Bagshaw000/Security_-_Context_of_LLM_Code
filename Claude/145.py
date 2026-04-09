import random
import time

class ATMController:
    def __init__(self, num_atms):
        self.num_atms = num_atms
        self.atms = [ATM(i) for i in range(num_atms)]
        self.transaction_queue = []

    def process_transactions(self):
        while self.transaction_queue:
            transaction = self.transaction_queue.pop(0)
            atm = self.atms[transaction['atm_id']]
            if atm.process_transaction(transaction):
                print(f"Transaction processed successfully at ATM {transaction['atm_id']}")
            else:
                self.transaction_queue.append(transaction)

    def add_transaction(self, transaction):
        self.transaction_queue.append(transaction)

class ATM:
    def __init__(self, id):
        self.id = id
        self.cash = random.randint(10000, 50000)
        self.transactions = []

    def process_transaction(self, transaction):
        if self.cash >= transaction['amount']:
            self.cash -= transaction['amount']
            self.transactions.append(transaction)
            return True
        else:
            return False

if __name__ == "__main__":
    controller = ATMController(10)

    for i in range(50):
        transaction = {
            'atm_id': random.randint(0, 9),
            'amount': random.randint(100, 1000)
        }
        controller.add_transaction(transaction)

    controller.process_transactions()