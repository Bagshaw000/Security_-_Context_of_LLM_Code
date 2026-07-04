import datetime
import random

class ATMController:
    def __init__(self, atm_network):
        self.atm_network = atm_network
        self.transaction_log = []

    def check_atm_status(self, atm_id):
        atm = self.atm_network.get(atm_id, None)
        if atm:
            return atm.get_status()
        else:
            return "ATM not found"

    def perform_transaction(self, atm_id, transaction_type, amount):
        atm = self.atm_network.get(atm_id, None)
        if atm:
            if transaction_type == "withdrawal":
                result = atm.withdraw_cash(amount)
            elif transaction_type == "deposit":
                result = atm.deposit_cash(amount)
            else:
                return "Invalid transaction type"

            if result:
                transaction = {
                    "atm_id": atm_id,
                    "transaction_type": transaction_type,
                    "amount": amount,
                    "timestamp": datetime.datetime.now()
                }
                self.transaction_log.append(transaction)
                return "Transaction successful"
            else:
                return "Transaction failed"
        else:
            return "ATM not found"

    def generate_report(self):
        report = {
            "total_transactions": len(self.transaction_log),
            "transactions_by_type": {
                "withdrawal": sum(1 for tx in self.transaction_log if tx["transaction_type"] == "withdrawal"),
                "deposit": sum(1 for tx in self.transaction_log if tx["transaction_type"] == "deposit")
            },
            "transactions_by_atm": {}
        }

        for tx in self.transaction_log:
            atm_id = tx["atm_id"]
            if atm_id in report["transactions_by_atm"]:
                report["transactions_by_atm"][atm_id] += 1
            else:
                report["transactions_by_atm"][atm_id] = 1

        return report

class ATM:
    def __init__(self, atm_id, location, cash_balance):
        self.atm_id = atm_id
        self.location = location
        self.cash_balance = cash_balance
        self.status = "online"

    def get_status(self):
        return self.status

    def withdraw_cash(self, amount):
        if self.cash_balance >= amount:
            self.cash_balance -= amount
            return True
        else:
            return False

    def deposit_cash(self, amount):
        self.cash_balance += amount
        return True


atm_network = {
    "atm1": ATM("atm1", "New York", 50000),
    "atm2": ATM("atm2", "London", 30000),
    "atm3": ATM("atm3", "Tokyo", 40000)
}

controller = ATMController(atm_network)


print(controller.check_atm_status("atm1"))  


print(controller.perform_transaction("atm1", "withdrawal", 1000))  
print(controller.perform_transaction("atm2", "deposit", 2000))  
print(controller.perform_transaction("atm3", "withdrawal", 5000))  


report = controller.generate_report()
print(report)