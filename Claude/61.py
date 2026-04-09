import pandas as pd
from datetime import datetime

def generate_reports(data_file, output_dir):
    
    data = pd.read_csv(data_file)
    
    
    income_statement = data.groupby('Account')['Amount'].sum().reset_index()
    income_statement['Report'] = 'Income Statement'
    income_statement.to_csv(f'{output_dir}/income_statement.csv', index=False)
    
    
    balance_sheet = data.groupby('Account')['Amount'].sum().reset_index()
    balance_sheet['Report'] = 'Balance Sheet'
    balance_sheet.to_csv(f'{output_dir}/balance_sheet.csv', index=False)
    
    
    cash_flow = data[data['Account'].isin(['Cash Receipts', 'Cash Payments'])]
    cash_flow = cash_flow.groupby('Account')['Amount'].sum().reset_index()
    cash_flow['Report'] = 'Cash Flow Statement'
    cash_flow.to_csv(f'{output_dir}/cash_flow.csv', index=False)

if __name__ == '__main__':
    generate_reports('accounting_data.csv', 'reports')