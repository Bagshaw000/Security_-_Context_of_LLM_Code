class ATM:
    def __init__(self, atm_id, location):
        self.atm_id = atm_id
        self.location = location
        self.balance = 0
        self.is_online = True

    def deposit(self, amount):
        if self.is_online:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if self.is_online and self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def check_balance(self):
        if self.is_online:
            return self.balance
        return None

    def set_online_status(self, status):
        self.is_online = status


class ATMController:
    def __init__(self):
        self.atms = {}

    def add_atm(self, atm):
        self.atms[atm.atm_id] = atm

    def remove_atm(self, atm_id):
        if atm_id in self.atms:
            del self.atms[atm_id]

    def deposit_to_atm(self, atm_id, amount):
        if atm_id in self.atms:
            return self.atms[atm_id].deposit(amount)
        return False

    def withdraw_from_atm(self, atm_id, amount):
        if atm_id in self.atms:
            return self.atms[atm_id].withdraw(amount)
        return False

    def check_balance_atm(self, atm_id):
        if atm_id in self.atms:
            return self.atms[atm_id].check_balance()
        return None

    def set_atm_status(self, atm_id, status):
        if atm_id in self.atms:
            self.atms[atm_id].set_online_status(status)



controller = ATMController()
atm1 = ATM("ATM001", "Location A")
controller.add_atm(atm1)

controller.deposit_to_atm("ATM001", 1000)
print(controller.check_balance_atm("ATM001"))  

controller.withdraw_from_atm("ATM001", 200)
print(controller.check_balance_atm("ATM001"))  

controller.set_atm_status("ATM001", False)
print(controller.withdraw_from_atm("ATM001", 100))  
```