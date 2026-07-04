import pandas as pd
from datetime import datetime

class AccountReport:
    def __init__(self, data):
        self.data = data

    def generate_report(self):
        
        self.data['Date'] = pd.to_datetime(self.data['Date'])

        
        self.data.sort_values(by='Date', inplace=True)

        
        self.data['Revenue'] = self.data.groupby('Date').transform(lambda x: sum(x['Revenue']))
        self.data['Expenses'] = self.data.groupby('Date').transform(lambda x: sum(x['Expenses']))

        
        self.data['Net Income'] = self.data['Revenue'] - self.data['Expenses']

        
        self.report = pd.DataFrame({
            'Year': self.data['Date'].dt.year,
            'Total Revenue': self.data.groupby('Date').transform(lambda x: sum(x['Revenue'])),
            'Total Expenses': self.data.groupby('Date').transform(lambda x: sum(x['Expenses'])),
            'Net Income': self.data.groupby('Date').transform(lambda x: x['Revenue'] - x['Expenses'])
        })

        
        return self.report

class EmployeeReport:
    def __init__(self, employee_data):
        self.employee_data = employee_data

    def generate_report(self):
        
        self.employee_data.sort_values(by='Experience', inplace=True)

        
        self.report = pd.DataFrame({
            'Role': self.employee_data['Role'].unique(),
            'Total Experience': self.employee_data.groupby('Role')['Experience'].transform(lambda x: sum(x))
        })

        
        return self.report

class AccountingReport:
    def __init__(self, account_data):
        self.account_data = account_data

    def generate_report(self):
        
        self.report = pd.DataFrame({
            'Category': self.account_data['Category'].unique(),
            'Total Revenue': self.account_data.groupby('Category')['Revenue'].sum()
        })

        
        return self.report


account_data = {
    'Date': ['2022-01-01', '2022-02-01', '2022-03-01'],
    'Category': ['A', 'B', 'C'],
    'Revenue': [1000, 2000, 3000],
    'Expenses': [500, 1000, 1500]
}

employee_data = {
    'Role': ['Software Engineer', 'Project Manager', 'Quality Assurance'],
    'Experience': [12, 10, 8]
}

account_report = AccountingReport(account_data)
employee_report = EmployeeReport(employee_data)

print(account_report.generate_report())
print(employee_report.generate_report())