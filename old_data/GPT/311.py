import pandas as pd


data = {
    'Patient ID': [1, 2],
    'age': [30, 45],
    'sex': ['M', 'F'],
    'procedure type': ['A', 'B'],
    'hour_1': [1, 2],
    'hour_2': [3, 4],
    'hour_3': [5, 6],
    'hour_4': [7, 8],
    'hour_5': [9, 10],
    'hour_6': [11, 12],
    'hour_7': [13, 14],
    'hour_8': [15, 16],
    'hour_9': [17, 18],
    'hour_10': [19, 20]
}

df = pd.DataFrame(data)


melted_df = df.melt(id_vars=['Patient ID', 'age', 'sex', 'procedure type'], 
                     value_vars=[f'hour_{i}' for i in range(1, 11)], 
                     var_name='Hour', 
                     value_name='Value')


melted_df['Time since surgery'] = melted_df['Hour'].str.extract('(\d+)').astype(int)


melted_df = melted_df.drop(columns=['Hour'])


final_df = melted_df[['Patient ID', 'age', 'sex', 'procedure type', 'Time since surgery', 'Value']]


final_df = final_df.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)

final_df