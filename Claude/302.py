import pandas as pd

df = pd.DataFrame()
df['Patient ID'] = [1, 1, 1, 2, 2, 2]
df['age'] = [50, 50, 50, 35, 35, 35]
df['sex'] = ['M', 'M', 'M', 'F', 'F', 'F']
df['procedure type'] = ['surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery']
df['1'] = [10, 12, 14, 8, 10, 12]
df['2'] = [11, 13, 15, 9, 11, 13]
df['3'] = [12, 14, 16, 10, 12, 14]
df['4'] = [13, 15, 17, 11, 13, 15]
df['5'] = [14, 16, 18, 12, 14, 16]
df['6'] = [15, 17, 19, 13, 15, 17]
df['7'] = [16, 18, 20, 14, 16, 18]
df['8'] = [17, 19, 21, 15, 17, 19]
df['9'] = [18, 20, 22, 16, 18, 20]
df['10'] = [19, 21, 23, 17, 19, 21]

new_df = pd.DataFrame()
new_df['Patient ID'] = df['Patient ID'].repeat(10)
new_df['Time since surgery'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * len(df)
new_df['age'] = df['age'].repeat(10)
new_df['sex'] = df['sex'].repeat(10)
new_df['procedure type'] = df['procedure type'].repeat(10)
for i in range(1, 11):
    new_df[i] = df[str(i)].values