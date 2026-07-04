import pandas as pd

df = pd.DataFrame({'Patient ID': [1, 1, 1, 2, 2, 2],
                   'age': [35, 35, 35, 45, 45, 45],
                   'sex': ['M', 'M', 'M', 'F', 'F', 'F'],
                   'procedure type': ['surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery'],
                   '1': [100, 90, 80, 95, 90, 85],
                   '2': [95, 85, 75, 90, 85, 80],
                   '3': [90, 80, 70, 85, 80, 75],
                   '4': [85, 75, 65, 80, 75, 70],
                   '5': [80, 70, 60, 75, 70, 65],
                   '6': [75, 65, 55, 70, 65, 60],
                   '7': [70, 60, 50, 65, 60, 55],
                   '8': [65, 55, 45, 60, 55, 50],
                   '9': [60, 50, 40, 55, 50, 45],
                   '10': [55, 45, 35, 50, 45, 40]})

new_df = pd.DataFrame(columns=['Patient ID', 'age', 'sex', 'procedure type', 'Time since surgery', 'value'])

for patient in df['Patient ID'].unique():
    patient_data = df[df['Patient ID'] == patient]
    for hour in range(1, 11):
        new_row = {'Patient ID': patient,
                   'age': patient_data['age'].iloc[0],
                   'sex': patient_data['sex'].iloc[0],
                   'procedure type': patient_data['procedure type'].iloc[0],
                   'Time since surgery': f"{hour} hour(s)",
                   'value': patient_data[str(hour)].iloc[0]}
        new_df = new_df.append(new_row, ignore_index=True)