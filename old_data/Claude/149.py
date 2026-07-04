import random

class ATMNetwork:
    def __init__(self, num_atms):
        self.atms = [ATM(i) for i in range(num_atms)]
        self.cash_reserve = 1000000  

    def monitor_atms(self):
        for atm in self.atms:
            if atm.cash_level < 20000:
                self.refill_atm(atm)

    def refill_atm(self, atm):
        if self.cash_reserve >= 50000:
            atm.cash_level = 50000
            self.cash_reserve -= 50000
        else:
            atm.cash_level = self.cash_reserve
            self.cash_reserve = 0

class ATM:
    def __init__(self, id):
        self.id = id
        self.cash_level = random.randint(20000, 50000)

    def dispense_cash(self, amount):
        if self.cash_level >= amount:
            self.cash_level -= amount
            return amount
        else:
            return 0


network = ATMNetwork(10)
while True:
    network.monitor_atms()
    for atm in network.atms:
        withdrawl_amount = random.randint(100, 5000)
        dispensed = atm.dispense_cash(withdrawl_amount)
        if dispensed > 0:
            print(f"ATM {atm.id} dispensed {dispensed} cash.")