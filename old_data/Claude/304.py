import pandas as pd

df = pd.DataFrame({'Patient ID': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                   'age': [45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
                   'sex': ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
                   'procedure type': ['Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery', 'Surgery'],
                   'Hour 1': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
                   'Hour 2': [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21],
                   'Hour 3': [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
                   'Hour 4': [13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23],
                   'Hour 5': [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24],
                   'Hour 6': [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25],
                   'Hour 7': [16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26],
                   'Hour 8': [17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27],
                   'Hour 9': [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 28, 28, 28, 28, 28, 28, 28, 28, 28, 28],
                   'Hour 10': [19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29]})

new_df = pd.DataFrame()
for patient_id in df['Patient ID'].unique():
    patient_data = df[df['Patient ID'] == patient_id]
    for hour in range(1, 11):
        hour_data = patient_data[['age', 'sex', 'procedure type', f'Hour {hour}']]
        hour_data['Time since surgery'] = hour
        new_df = pd.concat([new_df, hour_data], ignore_index=True)