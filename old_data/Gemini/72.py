







transactions = [
    {"date": "2023-11-01", "description": "Monthly Salary", "category": "Income", "amount": 4500.00},
    {"date": "2023-11-02", "description": "Rent Payment", "category": "Housing", "amount": -1200.00},
    {"date": "2023-11-05", "description": "Grocery Store", "category": "Food", "amount": -150.50},
    {"date": "2023-11-10", "description": "Private Tutoring", "category": "Income", "amount": 300.00},
    {"date": "2023-11-12", "description": "Electricity Bill", "category": "Utilities", "amount": -95.00},
    {"date": "2023-11-15", "description": "Internet Bill", "category": "Utilities", "amount": -60.00},
    {"date": "2023-11-20", "description": "Bookstore Purchase", "category": "Education", "amount": -45.00}
]


total_income = 0.0
total_expenses = 0.0


for item in transactions:
    amount = item["amount"]
    if amount > 0:
        
        total_income = total_income + amount
    else:
        
        total_expenses = total_expenses + amount


net_profit = total_income + total_expenses


print("===========================================")
print("        FINANCIAL SUMMARY REPORT           ")
print("===========================================")
print("DATE         DESCRIPTION          AMOUNT   ")
print("-------------------------------------------")


for item in transactions:
    date = item["date"]
    desc = item["description"]
    amt = item["amount"]
    
    print(f"{date}   {desc:<20} ${amt:>9.2f}")

print("-------------------------------------------")
print(f"TOTAL INCOME:              ${total_income:>10.2f}")
print(f"TOTAL EXPENSES:            ${abs(total_expenses):>10.2f}")
print("-------------------------------------------")
print(f"NET PROFIT (BALANCE):      ${net_profit:>10.2f}")
print("===========================================")


