import datetime
from collections import defaultdict

def generate_accounting_report(transactions):
    
    account_balances = defaultdict(float)

    
    for transaction in transactions:
        account, amount = transaction
        account_balances[account] += amount

    
    report = []
    report.append("Accounting Report")
    report.append("-" * 20)
    report.append("Account\tBalance")
    report.append("-" * 20)

    for account, balance in account_balances.items():
        report.append(f"{account}\t{balance:.2f}")

    report.append("-" * 20)
    report.append(f"Total\t{sum(account_balances.values()):.2f}")
    report.append("-" * 20)
    report.append(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return "\n".join(report)


transactions = [
    ("Cash", 1000.0),
    ("Accounts Receivable", 5000.0),
    ("Inventory", 2500.0),
    ("Accounts Payable", -3000.0),
    ("Rent Expense", -1200.0),
    ("Utilities Expense", -500.0)
]

report = generate_accounting_report(transactions)
print(report)