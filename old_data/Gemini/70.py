






transactions = [
    {"date": "2023-11-01", "description": "Tutoring Session", "amount": 150.00},
    {"date": "2023-11-02", "description": "Paper and Pens", "amount": -25.40},
    {"date": "2023-11-05", "description": "Monthly Rent", "amount": -900.00},
    {"date": "2023-11-10", "description": "Book Royalty Check", "amount": 420.00},
    {"date": "2023-11-15", "description": "Internet Bill", "amount": -55.00},
    {"date": "2023-11-20", "description": "Grading Assistant", "amount": -100.00}
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




print("========================================")
print("       MONTHLY FINANCIAL REPORT")
print("========================================")
print(f"{'DATE':<12} {'DESCRIPTION':<20} {'AMOUNT':>7}")
print("-" * 40)


for item in transactions:
    print(f"{item['date']:<12} {item['description']:<20} ${item['amount']:>7.2f}")

print("-" * 40)



print(f"Total Income:                ${total_income:>8.2f}")
print(f"Total Expenses:              ${abs(total_expenses):>8.2f}")
print("-" * 40)


if net_profit >= 0:
    print(f"NET PROFIT:                  ${net_profit:>8.2f}")
else:
    print(f"NET LOSS:                   (${abs(net_profit):>7.2f})")

print("========================================")



