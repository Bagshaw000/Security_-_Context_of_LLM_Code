import os
import datetime
from decimal import Decimal

def generate_income_statement(revenues, expenses):
    net_income = sum(revenues) - sum(expenses)
    return {
        'Revenues': revenues,
        'Expenses': expenses,
        'Net Income': net_income
    }

def generate_balance_sheet(assets, liabilities, equity):
    total_assets = sum(assets)
    total_liabilities = sum(liabilities)
    total_equity = sum(equity)
    return {
        'Assets': assets,
        'Liabilities': liabilities,
        'Equity': equity,
        'Total Assets': total_assets,
        'Total Liabilities': total_liabilities,
        'Total Equity': total_equity
    }

def generate_cash_flow_statement(operating_activities, investing_activities, financing_activities):
    net_cash_flow = (
        sum(operating_activities) +
        sum(investing_activities) +
        sum(financing_activities)
    )
    return {
        'Operating Activities': operating_activities,
        'Investing Activities': investing_activities,
        'Financing Activities': financing_activities,
        'Net Cash Flow': net_cash_flow
    }

def save_report(report, file_name):
    with open(file_name, 'w') as f:
        f.write(str(report))

if __name__ == '__main__':
    revenues = [Decimal('10000.00'), Decimal('12000.00'), Decimal('15000.00')]
    expenses = [Decimal('6000.00'), Decimal('7500.00'), Decimal('8000.00')]
    income_statement = generate_income_statement(revenues, expenses)
    save_report(income_statement, 'income_statement.txt')

    assets = [Decimal('50000.00'), Decimal('60000.00'), Decimal('70000.00')]
    liabilities = [Decimal('20000.00'), Decimal('25000.00'), Decimal('30000.00')]
    equity = [Decimal('30000.00'), Decimal('35000.00'), Decimal('40000.00')]
    balance_sheet = generate_balance_sheet(assets, liabilities, equity)
    save_report(balance_sheet, 'balance_sheet.txt')

    operating_activities = [Decimal('8000.00'), Decimal('9000.00'), Decimal('10000.00')]
    investing_activities = [Decimal('-5000.00'), Decimal('-6000.00'), Decimal('-7000.00')]
    financing_activities = [Decimal('2000.00'), Decimal('3000.00'), Decimal('4000.00')]
    cash_flow_statement = generate_cash_flow_statement(operating_activities, investing_activities, financing_activities)
    save_report(cash_flow_statement, 'cash_flow_statement.txt')