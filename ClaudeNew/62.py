import pandas as pd
import os
from datetime import datetime

def reorganize_patient_data(input_file, output_file=None):
    
    
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return None
    
    try:
        if input_file.endswith('.xlsx') or input_file.endswith('.xls'):
            df = pd.read_excel(input_file)
        else:
            df = pd.read_csv(input_file)
        
        print(f"Successfully loaded file with {len(df)} patients")
        print(f"Columns found: {list(df.columns)}")
        
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    
    try:
        patient_info_cols = []
        hour_cols = []
        
        for col in df.columns:
            if 'hour' in col.lower() or any(char.isdigit() for char in col):
                if 'hour' in col.lower():
                    hour_cols.append(col)
            else:
                patient_info_cols.append(col)
        
        hour_cols = sorted(hour_cols, key=lambda x: int(''.join(filter(str.isdigit, x))))
        
        if not hour_cols:
            print("Error: No hour columns found. Make sure columns are named 'Hour 1', 'Hour 2', etc.")
            return None
        
        print(f"Patient information columns: {patient_info_cols}")
        print(f"Hour columns found: {hour_cols}")
        
        new_rows = []
        
        for idx, row in df.iterrows():
            for hour_num, hour_col in enumerate(hour_cols, 1):
                new_row = {}
                
                for col in patient_info_cols:
                    new_row[col] = row[col]
                
                new_row['Time since surgery'] = hour_num
                new_row['Hour value'] = row[hour_col]
                
                new_rows.append(new_row)
        
        reorganized_df = pd.DataFrame(new_rows)
        
        col_order = ['Time since surgery'] + patient_info_cols + ['Hour value']
        reorganized_df = reorganized_df[col_order]
        
        print(f"\nReorganization successful!")
        print(f"Original data: {len(df)} rows, {len(df.columns)} columns")
        print(f"New data: {len(reorganized_df)} rows, {len(reorganized_df.columns)} columns")
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"patient_data_reorganized_{timestamp}.csv"
        
        backup_file = input_file.replace('.csv', '_backup.csv').replace('.xlsx', '_backup.xlsx')
        
        try:
            if input_file.endswith('.xlsx') or input_file.endswith('.xls'):
                df.to_excel(backup_file, index=False)
            else:
                df.to_csv(backup_file, index=False)
            print(f"Backup created: {backup_file}")
        except Exception as e:
            print(f"Warning: Could not create backup: {e}")
        
        reorganized_df.to_csv(output_file, index=False)
        print(f"Reorganized data saved to: {output_file}")
        
        return reorganized_df
        
    except Exception as e:
        print(f"Error during reorganization: {e}")
        return None

if __name__ == "__main__":
    input_filename = "patient_data.csv"
    result = reorganize_patient_data(input_filename)
    
    if result is not None:
        print("\nFirst few rows of reorganized data:")
        print(result.head(10))