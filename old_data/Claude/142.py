import random
import time

class ATMNetwork:
    def __init__(self, num_atms):
        self.atms = [ATM(i) for i in range(num_atms)]
        self.controller = Controller(self.atms)

    def run(self):
        while True:
            self.controller.monitor_atms()
            self.controller.adjust_cash_levels()
            time.sleep(60)  

class ATM:
    def __init__(self, id):
        self.id = id
        self.cash_level = random.randint(50000, 100000)

    def withdraw(self, amount):
        if self.cash_level >= amount:
            self.cash_level -= amount
            return True
        else:
            return False

class Controller:
    def __init__(self, atms):
        self.atms = atms
        self.target_cash_level = 75000

    def monitor_atms(self):
        for atm in self.atms:
            print(f"ATM {atm.id} cash level: {atm.cash_level}")

    def adjust_cash_levels(self):
        for atm in self.atms:
            if atm.cash_level < self.target_cash_level:
                amount_to_add = self.target_cash_level - atm.cash_level
                print(f"Refilling ATM {atm.id} with {amount_to_add}")
                atm.cash_level = self.target_cash_level
            elif atm.cash_level > self.target_cash_level:
                amount_to_remove = atm.cash_level - self.target_cash_level
                print(f"Removing {amount_to_remove} from ATM {atm.id}")
                atm.cash_level = self.target_cash_level

if __name__ == "__main__":
    network = ATMNetwork(10)
    network.run()