import pandas as pd
import numpy as np

data = {
    'Patient ID': [1, 2, 3],
    'age': [25, 30, 35],
    'sex': ['M', 'F', 'M'],
    'procedure type': ['Surgery', 'Procedure', 'Test'],
    'hour 1': [10, np.nan, 5],
    'hour 2': [8, 7, np.nan],
    'hour 3': [9, np.nan, 6],
    'hour 4': [np.nan, 10, 8],
    'hour 5': [7, np.nan, 12],
    'hour 6': [6, 9, np.nan],
    'hour 7': [5, np.nan, 11],
    'hour 8': [np.nan, 8, 10],
    'hour 9': [4, np.nan, 13],
    'hour 10': [3, np.nan, 14]
}

df = pd.DataFrame(data)

fixed_variables = ['Patient ID', 'age', 'sex', 'procedure type']

transformed_df = df[df[fixed_variables].notnull()].copy()

for column in df.columns:
    if column not in fixed_variables and df[column].dtype == float:
        transformed_df[f'Time since surgery {column}'] = df[column]
        transformed_df[column] = np.nan

print(transformed_df)