



transactions = [
    {"date": "2023-11-01", "description": "Tutoring Fee", "amount": 120.00, "type": "Income"},
    {"date": "2023-11-02", "description": "Notebooks", "amount": -35.50, "type": "Expense"},
    {"date": "2023-11-05", "description": "School Salary", "amount": 3200.00, "type": "Income"},
    {"date": "2023-11-10", "description": "Monthly Rent", "amount": -1000.00, "type": "Expense"},
    {"date": "2023-11-15", "description": "Art Supplies", "amount": -45.00, "type": "Expense"},
    {"date": "2023-11-20", "description": "Book Sale", "amount": 85.00, "type": "Income"}
]


total_income = 0
total_expenses = 0


print("FINANCIAL ACCOUNTING REPORT")
print("=" * 50)
print(f"{'Date':<12} {'Description':<22} {'Amount':>12}")
print("-" * 50)


for item in transactions:
    
    print(f"{item['date']:<12} {item['description']:<22} ${item['amount']:>11.2f}")
    
    
    if item['type'] == "Income":
        total_income = total_income + item['amount']
    
    else:
        total_expenses = total_expenses + item['amount']


net_profit = total_income + total_expenses


print("-" * 50)
print(f"Total Income:       ${total_income:>11.2f}")
print(f"Total Expenses:     ${abs(total_expenses):>11.2f}")
print("=" * 50)
print(f"NET PROFIT:         ${net_profit:>11.2f}")
print("=" * 50)