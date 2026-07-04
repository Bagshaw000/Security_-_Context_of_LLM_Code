import random

class ATMController:
    def __init__(self, num_atms):
        self.num_atms = num_atms
        self.atm_states = [True] * num_atms

    def check_atm_status(self, atm_id):
        return self.atm_states[atm_id]

    def update_atm_status(self, atm_id, status):
        self.atm_states[atm_id] = status

    def process_transaction(self, atm_id, amount):
        if self.check_atm_status(atm_id):
            print(f"Processing transaction of {amount} at ATM {atm_id}")
            
            self.update_atm_status(atm_id, random.choice([True, False]))
        else:
            print(f"ATM {atm_id} is currently unavailable.")


controller = ATMController(5)
controller.process_transaction(0, 100)
controller.process_transaction(2, 50)
controller.process_transaction(4, 75)