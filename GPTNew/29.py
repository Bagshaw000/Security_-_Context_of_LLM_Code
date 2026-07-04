class ATM:
    def __init__(self, atm_id, location, balance):
        self.atm_id = atm_id
        self.location = location
        self.balance = balance
        self.is_operational = True

    def withdraw(self, amount):
        if self.is_operational and amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def deposit(self, amount):
        if self.is_operational:
            self.balance += amount
            return True
        return False

    def check_balance(self):
        return self.balance

    def set_operational_status(self, status):
        self.is_operational = status


class ATMNetwork:
    def __init__(self):
        self.atms = {}

    def add_atm(self, atm):
        if atm.atm_id not in self.atms:
            self.atms[atm.atm_id] = atm

    def remove_atm(self, atm_id):
        if atm_id in self.atms:
            del self.atms[atm_id]

    def get_atm(self, atm_id):
        return self.atms.get(atm_id)

    def total_balance(self):
        return sum(atm.check_balance() for atm in self.atms.values())

    def operational_atms(self):
        return [atm for atm in self.atms.values() if atm.is_operational]


def main():
    network = ATMNetwork()
    
    atm1 = ATM("ATM001", "Location A", 1000)
    atm2 = ATM("ATM002", "Location B", 2000)
    
    network.add_atm(atm1)
    network.add_atm(atm2)

    atm1.withdraw(100)
    atm2.deposit(500)

    print("Total balance in network:", network.total_balance())
    print("Operational ATMs:", len(network.operational_atms()))


if __name__ == "__main__":
    main()