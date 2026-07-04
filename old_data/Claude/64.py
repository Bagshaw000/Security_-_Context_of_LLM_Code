import pandas as pd
import os

def generate_accounting_reports(data_dir):
    
    df = pd.read_csv(os.path.join(data_dir, 'financial_data.csv'))

    
    income_statement = df.groupby('account')['amount'].sum().reset_index()
    income_statement = income_statement.sort_values('amount', ascending=False)
    print(income_statement)

    
    balance_sheet = df.groupby('account_type')['amount'].sum().reset_index()
    balance_sheet = balance_sheet.sort_values('account_type')
    print(balance_sheet)

    
    cash_flow = df[df['account_type'] == 'cash']['amount'].sum()
    print(f'Cash Flow: {cash_flow}')

if __name__ == '__main__':
    generate_accounting_reports('path/to/data/directory')