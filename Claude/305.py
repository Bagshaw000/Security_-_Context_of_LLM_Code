import pandas as pd


new_df = pd.DataFrame()

for patient_id in df['Patient ID'].unique():
    patient_data = df[df['Patient ID'] == patient_id]
    for hour in range(1, 11):
        row = {
            'Time since surgery': f'Hour {hour}',
            'Patient ID': patient_id,
            'age': patient_data['age'].values[0],
            'sex': patient_data['sex'].values[0],
            'procedure type': patient_data['procedure type'].values[0],
            f'Hour {hour}': patient_data[f'Hour {hour}'].values[0]
        }
        new_df = new_df.append(row, ignore_index=True)