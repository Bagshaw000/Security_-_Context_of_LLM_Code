Here is the Python code to implement a controller system for a network of ATMs:

import time
import random

class ATM:
    def __init__(self, id, location, balance):
        self.id = id
        self.location = location
        self.balance = balance
        self.transactions = []

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append(("Withdrawal", amount))
            return True
        else:
            return False

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(("Deposit", amount))

class Controller:
    def __init__(self):
        self.atms = []

    def add_atm(self, atm):
        self.atms.append(atm)

    def monitor_atms(self):
        while True:
            for atm in self.atms:
                if random.randint(1, 100) < 10:
                    if random.randint(1, 2) == 1:
                        amount = random.randint(20, 500)
                        if atm.withdraw(amount):
                            print(f"ATM {atm.id} at {atm.location} dispensed {amount}")
                        else:
                            print(f"ATM {atm.id} at {atm.location} does not have enough cash")
                    else:
                        amount = random.randint(20, 500)
                        atm.deposit(amount)
                        print(f"ATM {atm.id} at {atm.location} received a deposit of {amount}")
            time.sleep(60)


controller = Controller()
atm1 = ATM(1, "Main Street", 10000)
atm2 = ATM(2, "Park Avenue", 15000)
atm3 = ATM(3, "Elm Street", 8000)

controller.add_atm(atm1)
controller.add_atm(atm2)
controller.add_atm(atm3)

controller.monitor_atms()