import csv
import os




filename = 'my_finances.csv'


if not os.path.exists(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Date', 'Description', 'Category', 'Amount'])
        
        writer.writerow(['2023-10-01', 'Monthly Salary', 'Income', '4500.00'])
        writer.writerow(['2023-10-02', 'House Rent', 'Housing', '-1200.00'])
        writer.writerow(['2023-10-05', 'Grocery Store', 'Food', '-150.50'])
        writer.writerow(['2023-10-10', 'Internet Bill', 'Utilities', '-60.00'])
        writer.writerow(['2023-10-15', 'Tutoring Income', 'Income', '300.00'])


total_money_in = 0
total_money_out = 0
category_totals = {}


with open(filename, mode='r') as file:
    
    spreadsheet = csv.DictReader(file)
    
    for row in spreadsheet:
        
        amount = float(row['Amount'])
        category = row['Category']
        
        
        if amount > 0:
            total_money_in = total_money_in + amount
        else:
            total_money_out = total_money_out + abs(amount)
        
        
        if category in category_totals:
            category_totals[category] = category_totals[category] + amount
        else:
            category_totals[category] = amount


final_balance = total_money_in - total_money_out


print("----------------------------------------")
print("        ANNUAL ACCOUNTING REPORT        ")
print("----------------------------------------")
print(f"Total Income:         ${total_money_in:,.2f}")
print(f"Total Expenses:       ${total_money_out:,.2f}")
print(f"Net Profit/Loss:      ${final_balance:,.2f}")
print("----------------------------------------")
print("BREAKDOWN BY CATEGORY:")

for category, amount in category_totals.items():
    
    print(f"- {category}: ${amount:,.2f}")

print("----------------------------------------")
print("Report Generation Complete.")