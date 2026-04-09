





transactions = [
    {"date": "2023-10-01", "description": "Monthly Salary", "category": "Income", "amount": 3500.00},
    {"date": "2023-10-02", "description": "Grocery Store", "category": "Food", "amount": -120.50},
    {"date": "2023-10-05", "description": "Rent Payment", "category": "Housing", "amount": -1100.00},
    {"date": "2023-10-10", "description": "Gas Station", "category": "Transport", "amount": -55.00},
    {"date": "2023-10-12", "description": "Internet Bill", "category": "Utilities", "amount": -80.00},
    {"date": "2023-10-15", "description": "Bookstore Purchase", "category": "Education", "amount": -45.00}
]



category_summaries = {}
total_balance = 0


for item in transactions:
    category = item["category"]
    amount = item["amount"]
    
    
    if category in category_summaries:
        category_summaries[category] += amount
    else:
        category_summaries[category] = amount
    
    
    total_balance += amount


print("==========================================")
print("       MONTHLY FINANCIAL REPORT           ")
print("==========================================")
print(f"{'CATEGORY':<20} | {'TOTAL AMOUNT':>15}")
print("------------------------------------------")


for category, total in category_summaries.items():
    
    print(f"{category:<20} | ${total:>14,.2f}")

print("------------------------------------------")
print(f"{'TOTAL BALANCE':<20} | ${total_balance:>14,.2f}")
print("==========================================")



