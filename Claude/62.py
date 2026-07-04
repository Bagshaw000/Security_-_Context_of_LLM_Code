import pandas as pd

df = pd.DataFrame({'Patient ID': [1, 1, 1, 2, 2, 2],
                   'age': [50, 50, 50, 35, 35, 35], 
                   'sex': ['M', 'M', 'M', 'F', 'F', 'F'],
                   'procedure type': ['surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery'],
                   'hour 1': [10, 15, 20, 5, 12, 18],
                   'hour 2': [12, 18, 22, 8, 15, 20],
                   'hour 3': [15, 20, 25, 10, 18, 22],
                   'hour 4': [18, 22, 28, 12, 20, 25],
                   'hour 5': [20, 25, 30, 15, 22, 28],
                   'hour 6': [22, 28, 32, 18, 25, 30],
                   'hour 7': [25, 30, 35, 20, 28, 32],
                   'hour 8': [28, 32, 38, 22, 30, 35],
                   'hour 9': [30, 35, 40, 25, 32, 38],
                   'hour 10': [32, 38, 42, 28, 35, 40]})

new_df = pd.DataFrame(columns=['Time since surgery', 'Patient ID', 'age', 'sex', 'procedure type'])

for patient_id in df['Patient ID'].unique():
    patient_data = df[df['Patient ID'] == patient_id]
    for hour in range(1, 11):
        new_row = {
            'Time since surgery': f'Hour {hour}',
            'Patient ID': patient_id,
            'age': patient_data['age'].iloc[0],
            'sex': patient_data['sex'].iloc[0],
            'procedure type': patient_data['procedure type'].iloc[0]
        }
        for col in range(1, 11):
            new_row[f'hour {col}'] = patient_data[f'hour {col}'].iloc[0]
        new_df = new_df.append(new_row, ignore_index=True)