import pandas as pd


data = {
    'Patient ID': [1, 2],
    'age': [30, 45],
    'sex': ['M', 'F'],
    'procedure type': ['A', 'B'],
    1: [2, 3],
    2: [4, 5],
    3: [6, 7],
    4: [8, 9],
    5: [10, 11],
    6: [12, 13],
    7: [14, 15],
    8: [16, 17],
    9: [18, 19],
    10: [20, 21]
}

df = pd.DataFrame(data)


melted_df = df.melt(id_vars=['Patient ID', 'age', 'sex', 'procedure type'], 
                     value_vars=list(range(1, 11)), 
                     var_name='Time since surgery', 
                     value_name='Value')


melted_df['Time since surgery'] = melted_df['Time since surgery'].astype(int)


final_df = melted_df.drop(columns=['Value'])


print(final_df)