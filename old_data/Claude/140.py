import random

class ATMController:
    def __init__(self, num_atms):
        self.num_atms = num_atms
        self.atm_states = [0] * num_atms
        self.atm_balances = [10000] * num_atms

    def check_atm_status(self, atm_id):
        return self.atm_states[atm_id]

    def check_atm_balance(self, atm_id):
        return self.atm_balances[atm_id]

    def update_atm_status(self, atm_id, status):
        self.atm_states[atm_id] = status

    def update_atm_balance(self, atm_id, amount):
        self.atm_balances[atm_id] += amount

    def process_transaction(self, atm_id, amount):
        if self.atm_states[atm_id] == 1 and self.atm_balances[atm_id] >= amount:
            self.atm_balances[atm_id] -= amount
            return True
        else:
            return False

    def monitor_atms(self):
        for i in range(self.num_atms):
            if random.randint(0, 100) < 5:
                self.atm_states[i] = 1 - self.atm_states[i]

controller = ATMController(100)

while True:
    atm_id = random.randint(0, 99)
    amount = random.randint(10, 500)
    if controller.process_transaction(atm_id, amount):
        print(f"Transaction successful at ATM {atm_id} for amount {amount}")
    else:
        print(f"Transaction failed at ATM {atm_id}")
    controller.monitor_atms()