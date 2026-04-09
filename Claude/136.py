import time
import random

class ATMNetwork:
    def __init__(self, num_atms):
        self.atms = [ATM(f"ATM{i+1}") for i in range(num_atms)]
        self.active_atms = self.atms.copy()

    def monitor_network(self):
        while True:
            for atm in self.active_atms:
                if random.random() < 0.05:
                    atm.report_issue()
                    self.active_atms.remove(atm)
                    print(f"{atm.name} has encountered an issue and has been removed from the active network.")
            time.sleep(60)

class ATM:
    def __init__(self, name):
        self.name = name

    def report_issue(self):
        print(f"{self.name} is reporting an issue.")

if __name__ == "__main__":
    network = ATMNetwork(50)
    network.monitor_network()