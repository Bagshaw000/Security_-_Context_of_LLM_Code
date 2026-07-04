import pandas as pd


file_path = 'patients.xlsx'  
df = pd.read_excel(file_path)


rearranged_data = []


for index, row in df.iterrows():
    patient_id = row['Patient ID']
    age = row['age']
    sex = row['sex']
    procedure_type = row['procedure type']
    
    
    for hour in range(1, 11):
        time_since_surgery = f'Hour {hour}'
        hours_value = row[f'hours {hour}']
        
        rearranged_data.append({
            'Patient ID': patient_id,
            'age': age,
            'sex': sex,
            'procedure type': procedure_type,
            'Time since surgery': time_since_surgery,
            'hours value': hours_value
        })


new_df = pd.DataFrame(rearranged_data)


new_file_path = 'rearranged_patients.xlsx'  
new_df.to_excel(new_file_path, index=False)