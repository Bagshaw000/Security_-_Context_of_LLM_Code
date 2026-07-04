class ATM:
    def __init__(self, id, balance):
        self.id = id
        self.balance = balance

class Transaction:
    def __init__(self, amount, atm_id, type):
        self.amount = amount
        self.atm_id = atm_id
        self.type = type

class Controller:
    def __init__(self):
        self.atms = {}
        self.transactions = []

    def add_atm(self, id, balance):
        self.atms[id] = ATM(id, balance)

    def process_transaction(self, amount, atm_id, transaction_type):
        if amount <= 0 or atm_id not in self.atms:
            return False

        atm = self.atms[atm_id]
        if transaction_type == 'deposit':
            atm.balance += amount
        elif transaction_type == 'withdrawal':
            if atm.balance >= amount:
                atm.balance -= amount
                self.transactions.append(Transaction(amount, atm_id, transaction_type))
                return True
            else:
                return False

    def get_balance(self, atm_id):
        return self.atms[atm_id].balance

    def view_transactions(self):
        for transaction in self.transactions:
            print(f"Transaction Type: {transaction.type}, Amount: {transaction.amount}, ATM ID: {transaction.atm_id}")


controller = Controller()
controller.add_atm(1, 1000)
controller.add_atm(2, 2000)

print("Initial balance of ATM 1:", controller.get_balance(1))
print("Initial balance of ATM 2:", controller.get_balance(2))

controller.process_transaction(500, 1, 'deposit')
print("Balance of ATM 1 after deposit:", controller.get_balance(1))

controller.process_transaction(1000, 1, 'withdrawal')
controller.process_transaction(200, 2, 'deposit')

controller.view_transactions()