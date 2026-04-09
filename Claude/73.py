import pandas as pd
import datetime

def generate_monthly_report(data, month, year):
    df = data[data['date'].dt.month == month]
    df = df[data['date'].dt.year == year]
    
    total_revenue = df['revenue'].sum()
    total_expenses = df['expenses'].sum()
    net_income = total_revenue - total_expenses
    
    report = {
        'month': datetime.date(year, month, 1).strftime('%B'),
        'year': year,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_income': net_income
    }
    
    return report

def generate_annual_report(data, year):
    df = data[data['date'].dt.year == year]
    
    total_revenue = df['revenue'].sum()
    total_expenses = df['expenses'].sum()
    net_income = total_revenue - total_expenses
    
    report = {
        'year': year,
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_income': net_income
    }
    
    return report


data = pd.read_csv('accounting_data.csv')
data['date'] = pd.to_datetime(data['date'])

monthly_report = generate_monthly_report(data, 6, 2022)
print(monthly_report)

annual_report = generate_annual_report(data, 2022)
print(annual_report)