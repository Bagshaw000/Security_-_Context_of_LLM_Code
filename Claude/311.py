import pandas as pd


new_df = pd.DataFrame(columns=['Time since surgery', 'Patient ID', 'age', 'sex', 'procedure type'])

for patient in df['Patient ID'].unique():
    patient_data = df[df['Patient ID'] == patient]
    for hour in range(1, 11):
        row = {
            'Time since surgery': f'{hour} hour(s)',
            'Patient ID': patient,
            'age': patient_data['age'].iloc[0],
            'sex': patient_data['sex'].iloc[0],
            'procedure type': patient_data['procedure type'].iloc[0],
            f'Hour {hour}': patient_data[f'Hour {hour}'].iloc[0]
        }
        new_df = new_df.append(row, ignore_index=True)