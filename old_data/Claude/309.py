import pandas as pd

df = pd.DataFrame({'Patient ID': [1, 1, 1, 2, 2, 2],
                   'age': [50, 50, 50, 35, 35, 35],
                   'sex': ['M', 'M', 'M', 'F', 'F', 'F'],
                   'procedure type': ['Surgery A', 'Surgery A', 'Surgery A', 'Surgery B', 'Surgery B', 'Surgery B'],
                   'Hour 1': [10, 12, 8, 15, 18, 13],
                   'Hour 2': [12, 14, 10, 14, 16, 12],
                   'Hour 3': [14, 16, 12, 13, 15, 11],
                   'Hour 4': [16, 18, 14, 12, 14, 10],
                   'Hour 5': [18, 20, 16, 11, 13, 9],
                   'Hour 6': [20, 22, 18, 10, 12, 8],
                   'Hour 7': [22, 24, 20, 9, 11, 7],
                   'Hour 8': [24, 26, 22, 8, 10, 6],
                   'Hour 9': [26, 28, 24, 7, 9, 5],
                   'Hour 10': [28, 30, 26, 6, 8, 4]})

new_df = pd.DataFrame()

for patient_id in df['Patient ID'].unique():
    patient_data = df[df['Patient ID'] == patient_id]
    for hour in range(1, 11):
        hour_data = patient_data.loc[:, [f'Hour {hour}']].rename(columns={f'Hour {hour}': 'Value'})
        hour_data['Time since surgery'] = hour
        hour_data['Patient ID'] = patient_id
        hour_data['age'] = patient_data['age'].iloc[0]
        hour_data['sex'] = patient_data['sex'].iloc[0]
        hour_data['procedure type'] = patient_data['procedure type'].iloc[0]
        new_df = pd.concat([new_df, hour_data], ignore_index=True)