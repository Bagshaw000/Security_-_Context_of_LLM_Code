





transactions = [
    {"date": "Oct 01", "description": "Monthly Salary", "amount": 4000.00},
    {"date": "Oct 02", "description": "House Rent", "amount": -1500.00},
    {"date": "Oct 05", "description": "Grocery Store", "amount": -245.50},
    {"date": "Oct 08", "description": "Tutoring Income", "amount": 150.00},
    {"date": "Oct 12", "description": "Electricity Bill", "amount": -85.00},
    {"date": "Oct 15", "description": "Internet Bill", "amount": -60.00},
    {"date": "Oct 20", "description": "Bookstore", "amount": -45.00}
]



total_income = 0.0
total_expenses = 0.0

for item in transactions:
    value = item["amount"]
    if value > 0:
        
        total_income = total_income + value
    else:
        
        total_expenses = total_expenses + value


final_balance = total_income + total_expenses



print("============================================")
print("         FINANCIAL SUMMARY REPORT           ")
print("============================================")
print(f"{'DATE':<10} {'DESCRIPTION':<20} {'AMOUNT':>10}")
print("--------------------------------------------")

for item in transactions:
    
    print(f"{item['date']:<10} {item['description']:<20} {item['amount']:>10.2f}")

print("--------------------------------------------")
print(f"TOTAL INCOME:               ${total_income:>10.2f}")
print(f"TOTAL EXPENSES:             ${abs(total_expenses):>10.2f}")
print("--------------------------------------------")
print(f"NET FINAL BALANCE:          ${final_balance:>10.2f}")
print("============================================")

