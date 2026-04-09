import time
import random

class ATMController:
    def __init__(self, num_atms):
        self.atms = [ATM(i) for i in range(num_atms)]
        self.transaction_queue = []
        self.transaction_timeout = 60  

    def process_transactions(self):
        while self.transaction_queue:
            transaction = self.transaction_queue.pop(0)
            atm = self.atms[transaction.atm_id]
            if atm.process_transaction(transaction):
                print(f"Transaction successful: {transaction}")
            else:
                self.transaction_queue.append(transaction)

        for atm in self.atms:
            atm.check_for_maintenance()

    def add_transaction(self, transaction):
        self.transaction_queue.append(transaction)

    def run(self):
        while True:
            self.process_transactions()
            time.sleep(1)

class ATM:
    def __init__(self, atm_id):
        self.atm_id = atm_id
        self.cash = 10000
        self.last_maintenance = time.time()
        self.maintenance_interval = 3600  

    def process_transaction(self, transaction):
        if self.cash >= transaction.amount:
            self.cash -= transaction.amount
            return True
        else:
            return False

    def check_for_maintenance(self):
        if time.time() - self.last_maintenance >= self.maintenance_interval:
            self.perform_maintenance()

    def perform_maintenance(self):
        print(f"ATM {self.atm_id} is undergoing maintenance.")
        self.cash = 10000
        self.last_maintenance = time.time()

class Transaction:
    def __init__(self, atm_id, amount):
        self.atm_id = atm_id
        self.amount = amount

    def __str__(self):
        return f"Transaction: ATM {self.atm_id}, Amount: {self.amount}"


controller = ATMController(10)

while True:
    atm_id = random.randint(0, 9)
    amount = random.randint(50, 500)
    transaction = Transaction(atm_id, amount)
    controller.add_transaction(transaction)
    time.sleep(random.uniform(0.5, 2))