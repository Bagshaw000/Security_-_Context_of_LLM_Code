import pandas as pd


data = {
    'Patient ID': [1, 2],
    'age': [30, 45],
    'sex': ['M', 'F'],
    'procedure type': ['A', 'B'],
    'hour_1': [5, 3],
    'hour_2': [6, 4],
    'hour_3': [7, 5],
    'hour_4': [8, 6],
    'hour_5': [9, 7],
    'hour_6': [10, 8],
    'hour_7': [11, 9],
    'hour_8': [12, 10],
    'hour_9': [13, 11],
    'hour_10': [14, 12]
}

df = pd.DataFrame(data)


melted_df = df.melt(id_vars=['Patient ID', 'age', 'sex', 'procedure type'], 
                     value_vars=[f'hour_{i}' for i in range(1, 11)],
                     var_name='Hour', 
                     value_name='Value')


melted_df['Time since surgery'] = melted_df['Hour'].str.extract('(\d+)').astype(int)
final_df = melted_df[['Patient ID', 'age', 'sex', 'procedure type', 'Time since surgery', 'Value']]


print(final_df)