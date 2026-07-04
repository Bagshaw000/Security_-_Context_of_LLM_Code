import pandas as pd
import os

def generate_accounting_reports(input_dir, output_dir):
    
    
    os.makedirs(output_dir, exist_ok=True)

    
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            
            df = pd.read_csv(os.path.join(input_dir, filename))

            
            sales_report = generate_sales_report(df)
            expense_report = generate_expense_report(df)
            profit_report = generate_profit_report(df)

            
            sales_report.to_csv(os.path.join(output_dir, "sales_report.csv"), index=False)
            expense_report.to_csv(os.path.join(output_dir, "expense_report.csv"), index=False)
            profit_report.to_csv(os.path.join(output_dir, "profit_report.csv"), index=False)

def generate_sales_report(df):
    
    sales_report = df.groupby("product")["revenue"].sum().reset_index()
    sales_report = sales_report.sort_values("revenue", ascending=False)
    return sales_report

def generate_expense_report(df):
    
    expense_report = df.groupby("expense_category")["expense"].sum().reset_index()
    expense_report = expense_report.sort_values("expense", ascending=False)
    return expense_report

def generate_profit_report(df):
    
    profit_report = df[["product", "revenue", "expense"]]
    profit_report["profit"] = profit_report["revenue"] - profit_report["expense"]
    profit_report = profit_report.sort_values("profit", ascending=False)
    return profit_report