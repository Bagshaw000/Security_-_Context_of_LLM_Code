import pandas as pd
from datetime import datetime

def generate_accounting_reports(data_file):
    
    df = pd.read_csv(data_file)
    
    
    total_revenue = df['Revenue'].sum()
    total_expenses = df['Expenses'].sum()
    
    
    net_profit = total_revenue - total_expenses
    
    
    income_statement = pd.DataFrame({
        'Item': ['Revenue', 'Expenses', 'Net Profit'],
        'Amount': [total_revenue, total_expenses, net_profit]
    })
    
    
    balance_sheet = pd.DataFrame({
        'Asset': ['Cash', 'Accounts Receivable', 'Inventory', 'Total Assets'],
        'Amount': [df['Cash'].sum(), df['Accounts Receivable'].sum(), df['Inventory'].sum(), df['Cash'].sum() + df['Accounts Receivable'].sum() + df['Inventory'].sum()]
    })
    balance_sheet = balance_sheet.append({
        'Asset': 'Liabilities',
        'Amount': df['Accounts Payable'].sum()
    }, ignore_index=True)
    balance_sheet = balance_sheet.append({
        'Asset': 'Equity',
        'Amount': balance_sheet['Amount'].sum() - df['Accounts Payable'].sum()
    }, ignore_index=True)
    
    
    cash_flow_statement = pd.DataFrame({
        'Item': ['Net Profit', 'Depreciation', 'Change in Accounts Receivable', 'Change in Inventory', 'Change in Accounts Payable', 'Net Cash Flow'],
        'Amount': [net_profit, df['Depreciation'].sum(), df['Accounts Receivable'].diff().sum(), df['Inventory'].diff().sum(), df['Accounts Payable'].diff().sum(), df['Cash'].diff().sum()]
    })
    
    
    return {
        'Income Statement': income_statement,
        'Balance Sheet': balance_sheet,
        'Cash Flow Statement': cash_flow_statement
    }


reports = generate_accounting_reports('accounting_data.csv')
for report_name, report_df in reports.items():
    print(f'{report_name}:\n{report_df}\n')