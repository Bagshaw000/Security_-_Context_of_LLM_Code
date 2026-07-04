import pandas as pd


data = {
    'Patient ID': [1, 2],
    'age': [30, 45],
    'sex': ['M', 'F'],
    'procedure type': ['A', 'B'],
    'hour_1': [1, 2],
    'hour_2': [2, 3],
    'hour_3': [3, 4],
    'hour_4': [4, 5],
    'hour_5': [5, 6],
    'hour_6': [6, 7],
    'hour_7': [7, 8],
    'hour_8': [8, 9],
    'hour_9': [9, 10],
    'hour_10': [10, 11]
}

df = pd.DataFrame(data)


melted_df = df.melt(id_vars=['Patient ID', 'age', 'sex', 'procedure type'], 
                     value_vars=[f'hour_{i}' for i in range(1, 11)], 
                     var_name='Hour', 
                     value_name='Time since surgery')


melted_df['Hour'] = melted_df['Hour'].str.extract('(\d+)').astype(int)


melted_df = melted_df.rename(columns={'Hour': 'Time since surgery'})


final_df = melted_df[['Patient ID', 'age', 'sex', 'procedure type', 'Time since surgery', 'Time since surgery']]


print(final_df)