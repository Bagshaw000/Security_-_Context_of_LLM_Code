class ATM:
    def __init__(self, atm_id, balance):
        self.atm_id = atm_id
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited: {amount}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.transactions.append(f"Withdrew: {amount}")
            return True
        return False

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions


class ATMController:
    def __init__(self):
        self.atms = {}

    def add_atm(self, atm_id, initial_balance):
        self.atms[atm_id] = ATM(atm_id, initial_balance)

    def deposit(self, atm_id, amount):
        if atm_id in self.atms:
            self.atms[atm_id].deposit(amount)

    def withdraw(self, atm_id, amount):
        if atm_id in self.atms:
            return self.atms[atm_id].withdraw(amount)
        return False

    def get_balance(self, atm_id):
        if atm_id in self.atms:
            return self.atms[atm_id].get_balance()
        return None

    def get_transactions(self, atm_id):
        if atm_id in self.atms:
            return self.atms[atm_id].get_transactions()
        return None



controller = ATMController()
controller.add_atm("ATM1", 1000)
controller.deposit("ATM1", 200)
if controller.withdraw("ATM1", 150):
    print("Withdrawal successful")
else:
    print("Insufficient funds")

print("Balance:", controller.get_balance("ATM1"))
print("Transactions:", controller.get_transactions("ATM1"))