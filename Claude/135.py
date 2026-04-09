import random
import time

class ATMController:
    def __init__(self, num_atms):
        self.num_atms = num_atms
        self.atms = [ATM(i) for i in range(num_atms)]
        self.balances = [1000000 for _ in range(num_atms)]

    def run(self):
        while True:
            for i, atm in enumerate(self.atms):
                self.process_transaction(i, atm)
            time.sleep(1)

    def process_transaction(self, atm_id, atm):
        if random.random() < 0.1:
            amount = random.randint(100, 10000)
            if self.balances[atm_id] >= amount:
                self.balances[atm_id] -= amount
                atm.dispense_cash(amount)
            else:
                atm.report_low_balance()

class ATM:
    def __init__(self, id):
        self.id = id

    def dispense_cash(self, amount):
        print(f"ATM {self.id} dispensed ${amount}")

    def report_low_balance(self):
        print(f"ATM {self.id} is low on cash")

controller = ATMController(10)
controller.run()