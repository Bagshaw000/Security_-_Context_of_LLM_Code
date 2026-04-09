import pandas as pd

df = pd.DataFrame()
df['Patient ID'] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
df['age'] = [45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
df['sex'] = ['M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'M', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F']
df['procedure type'] = ['surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery']
df['1'] = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6]
df['2'] = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5]
df['3'] = [8, 7, 6, 5, 4, 3, 2, 1, 0, -1, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4]
df['4'] = [7, 6, 5, 4, 3, 2, 1, 0, -1, -2, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3]
df['5'] = [6, 5, 4, 3, 2, 1, 0, -1, -2, -3, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
df['6'] = [5, 4, 3, 2, 1, 0, -1, -2, -3, -4, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
df['7'] = [4, 3, 2, 1, 0, -1, -2, -3, -4, -5, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
df['8'] = [3, 2, 1, 0, -1, -2, -3, -4, -5, -6, 8, 7, 6, 5, 4, 3, 2, 1, 0, -1]
df['9'] = [2, 1, 0, -1, -2, -3, -4, -5, -6, -7, 7, 6, 5, 4, 3, 2, 1, 0, -1, -2]
df['10'] = [1, 0, -1, -2, -3, -4, -5, -6, -7, -8, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3]

result = pd.DataFrame()
for idx, row in df.iterrows():
    patient_id = row['Patient ID']
    for i in range(1, 11):
        new_row = row.copy()
        new_row['Time since surgery'] = row[str(i)]
        new_row['Hour'] = i
        result = result.append(new_row, ignore_index=True)

print(result)