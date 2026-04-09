import random
import time

class ATMController:
    def __init__(self, num_atms):
        self.num_atms = num_atms
        self.atm_states = [0] * num_atms
        self.transaction_queue = []

    def process_transaction(self, atm_id, transaction):
        time.sleep(random.uniform(0.5, 2.0))
        self.atm_states[atm_id] = 0
        print(f"Processed transaction at ATM {atm_id}: {transaction}")

    def add_transaction(self, atm_id, transaction):
        self.atm_states[atm_id] = 1
        self.transaction_queue.append((atm_id, transaction))

    def run(self):
        while True:
            if self.transaction_queue:
                atm_id, transaction = self.transaction_queue.pop(0)
                self.process_transaction(atm_id, transaction)
            else:
                for i in range(self.num_atms):
                    if self.atm_states[i] == 0 and random.random() < 0.1:
                        self.add_transaction(i, f"Transaction {len(self.transaction_queue)}")
                time.sleep(0.1)

controller = ATMController(10)
controller.run()