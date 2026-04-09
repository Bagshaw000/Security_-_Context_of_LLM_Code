import pandas as pd

df = pd.DataFrame()
df['Patient ID'] = [1, 1, 1, 2, 2, 2]
df['age'] = [50, 50, 50, 60, 60, 60]
df['sex'] = ['M', 'M', 'M', 'F', 'F', 'F']
df['procedure type'] = ['surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery']
df['1'] = [100, 90, 80, 110, 100, 95]
df['2'] = [95, 85, 75, 105, 95, 90]
df['3'] = [90, 80, 70, 100, 90, 85]
df['4'] = [85, 75, 65, 95, 85, 80]
df['5'] = [80, 70, 60, 90, 80, 75]
df['6'] = [75, 65, 55, 85, 75, 70]
df['7'] = [70, 60, 50, 80, 70, 65]
df['8'] = [65, 55, 45, 75, 65, 60]
df['9'] = [60, 50, 40, 70, 60, 55]
df['10'] = [55, 45, 35, 65, 55, 50]

new_df = pd.DataFrame(columns=['Patient ID', 'Time since surgery', 'age', 'sex', 'procedure type'])

for patient in df['Patient ID'].unique():
    patient_data = df[df['Patient ID'] == patient]
    for hour in range(1, 11):
        new_row = {
            'Patient ID': patient,
            'Time since surgery': hour,
            'age': patient_data['age'].iloc[0],
            'sex': patient_data['sex'].iloc[0],
            'procedure type': patient_data['procedure type'].iloc[0],
            hour: patient_data[str(hour)].iloc[0]
        }
        new_df = new_df.append(new_row, ignore_index=True)