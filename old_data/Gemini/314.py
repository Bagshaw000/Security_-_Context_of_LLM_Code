import pandas as pd

data = {
    'Patient ID': [1, 2],
    'age': [45, 60],
    'sex': ['Male', 'Female'],
    'procedure type': ['Type A', 'Type B'],
    '1': [10, 20], '2': [11, 21], '3': [12, 22], '4': [13, 23], '5': [14, 24],
    '6': [15, 25], '7': [16, 26], '8': [17, 27], '9': [18, 28], '10': [19, 29]
}
df = pd.DataFrame(data)

fixed_variables = ['Patient ID', 'age', 'sex', 'procedure type']
hour_columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

df_reorganised = pd.melt(
    df, 
    id_vars=fixed_variables, 
    value_vars=hour_columns, 
    var_name='Time since surgery', 
    value_name='Measurement'
)

column_order = ['Time since surgery'] + fixed_variables + ['Measurement']
df_reorganised = df_reorganised[column_order]

df_reorganised = df_reorganised.sort_values(by=['Patient ID', 'Time since surgery'])

print(df_reorganised)