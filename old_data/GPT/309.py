import pandas as pd


data = {
    'Patient ID': [1, 2],
    'age': [30, 45],
    'sex': ['M', 'F'],
    'procedure type': ['A', 'B'],
    1: [2, 3],
    2: [1, 2],
    3: [0, 1],
    4: [0, 0],
    5: [0, 0],
    6: [0, 0],
    7: [0, 0],
    8: [0, 0],
    9: [0, 0],
    10: [0, 0]
}

df = pd.DataFrame(data)


melted_df = df.melt(id_vars=['Patient ID', 'age', 'sex', 'procedure type'], 
                     value_vars=list(range(1, 11)), 
                     var_name='Hour', 
                     value_name='Value')


melted_df = melted_df[melted_df['Value'] > 0]


melted_df['Time since surgery'] = melted_df['Hour'].astype(int)


final_df = melted_df[['Patient ID', 'age', 'sex', 'procedure type', 'Time since surgery', 'Value']]


final_df = final_df.drop(columns=['Hour'])


final_df.reset_index(drop=True, inplace=True)

print(final_df)