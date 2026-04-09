import threading
import random
import time

class ATM:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance
        self.status = "online"

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"ATM {self.id} dispensed {amount}")
        else:
            print(f"ATM {self.id} has insufficient funds")

    def set_status(self, status):
        self.status = status
        print(f"ATM {self.id} status changed to {status}")

class ATMController:
    def __init__(self, atms):
        self.atms = atms
        self.monitor_thread = threading.Thread(target=self.monitor_atms)
        self.monitor_thread.start()

    def monitor_atms(self):
        while True:
            for atm in self.atms:
                if atm.status == "online" and random.random() < 0.1:
                    atm.set_status("offline")
                elif atm.status == "offline" and random.random() < 0.05:
                    atm.set_status("online")
                amount = random.randint(10, 500)
                atm.withdraw(amount)
            time.sleep(1)


atms = [
    ATM(1, 10000),
    ATM(2, 15000),
    ATM(3, 20000),
    ATM(4, 8000),
    ATM(5, 12000)
]

controller = ATMController(atms)