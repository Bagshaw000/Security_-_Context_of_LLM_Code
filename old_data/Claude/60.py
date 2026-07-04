import datetime
import pandas as pd

def generate_sales_report(sales_data, start_date, end_date):
    
    report_data = sales_data[(sales_data['date'] >= start_date) & (sales_data['date'] <= end_date)]
    report_data = report_data.groupby('product')['revenue'].sum().reset_index()
    report_data = report_data.sort_values('revenue', ascending=False)
    return report_data

def generate_expense_report(expense_data, start_date, end_date):
    
    report_data = expense_data[(expense_data['date'] >= start_date) & (expense_data['date'] <= end_date)]
    report_data = report_data.groupby('category')['amount'].sum().reset_index()
    report_data = report_data.sort_values('amount', ascending=False)
    return report_data

def generate_profit_and_loss_statement(sales_data, expense_data, start_date, end_date):
    
    sales_report = generate_sales_report(sales_data, start_date, end_date)
    expense_report = generate_expense_report(expense_data, start_date, end_date)
    
    total_revenue = sales_report['revenue'].sum()
    total_expenses = expense_report['amount'].sum()
    net_profit = total_revenue - total_expenses
    
    profit_and_loss = pd.DataFrame({
        'Item': ['Total Revenue', 'Total Expenses', 'Net Profit'],
        'Amount': [total_revenue, total_expenses, net_profit]
    })
    
    return profit_and_loss