import random
import time

class ATMController:
    def __init__(self, num_atms):
        self.atms = [ATM(i) for i in range(num_atms)]
        self.transactions = []

    def process_transaction(self, atm_id, amount):
        atm = self.atms[atm_id]
        if atm.has_sufficient_funds(amount):
            atm.dispense_cash(amount)
            self.transactions.append((atm_id, amount))
            return True
        else:
            return False

    def monitor_atms(self):
        while True:
            for atm in self.atms:
                if atm.needs_refilling():
                    self.refill_atm(atm.id)
            time.sleep(60)

    def refill_atm(self, atm_id):
        atm = self.atms[atm_id]
        atm.refill()
        print(f"ATM {atm_id} has been refilled.")

class ATM:
    def __init__(self, id):
        self.id = id
        self.cash_on_hand = random.randint(10000, 50000)

    def has_sufficient_funds(self, amount):
        return self.cash_on_hand >= amount

    def dispense_cash(self, amount):
        self.cash_on_hand -= amount

    def needs_refilling(self):
        return self.cash_on_hand < 10000

    def refill(self):
        self.cash_on_hand = 50000

if __name__ == "__main__":
    controller = ATMController(10)
    controller.process_transaction(0, 500)
    controller.process_transaction(5, 1000)
    controller.monitor_atms()