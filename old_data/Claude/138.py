import time
import random

class ATMNetwork:
    def __init__(self, num_atms):
        self.atms = [ATM(i) for i in range(num_atms)]
        self.controller = ATMController(self.atms)

    def run(self):
        while True:
            self.controller.monitor_atms()
            time.sleep(5)

class ATM:
    def __init__(self, id):
        self.id = id
        self.cash_level = random.randint(50, 500)
        self.error_status = False

    def dispense_cash(self, amount):
        if self.cash_level >= amount:
            self.cash_level -= amount
            return True
        else:
            return False

    def report_error(self):
        self.error_status = True

class ATMController:
    def __init__(self, atms):
        self.atms = atms

    def monitor_atms(self):
        for atm in self.atms:
            if atm.cash_level < 100:
                self.refill_atm(atm)
            if atm.error_status:
                self.resolve_error(atm)

    def refill_atm(self, atm):
        print(f"Refilling ATM {atm.id} with cash.")
        atm.cash_level = 500

    def resolve_error(self, atm):
        print(f"Resolving error on ATM {atm.id}.")
        atm.error_status = False

if __name__ == "__main__":
    network = ATMNetwork(10)
    network.run()