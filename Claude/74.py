import os
import pandas as pd

def generate_sales_report(data_file, output_file):
    
    
    data = pd.read_csv(data_file)
    
    
    total_sales = data['sales'].sum()
    sales_by_product = data.groupby('product')['sales'].sum().sort_values(ascending=False)
    
    
    report = f"Total Sales: {total_sales:.2f}\n\nSales by Product:\n{sales_by_product}"
    
    
    with open(output_file, 'w') as f:
        f.write(report)

def generate_expense_report(data_file, output_file):
    
    
    data = pd.read_csv(data_file)
    
    
    total_expenses = data['amount'].sum()
    expenses_by_category = data.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    
    report = f"Total Expenses: {total_expenses:.2f}\n\nExpenses by Category:\n{expenses_by_category}"
    
    
    with open(output_file, 'w') as f:
        f.write(report)


generate_sales_report('sales_data.csv', 'sales_report.txt')
generate_expense_report('expense_data.csv', 'expense_report.txt')