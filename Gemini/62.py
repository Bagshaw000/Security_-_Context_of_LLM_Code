import pandas as pd



example_data = {
    'Patient ID': [101, 102],
    'age': [45, 67],
    'sex': ['Male', 'Female'],
    'procedure type': ['Appendectomy', 'Knee Replacement'],
    '1': [70, 72], '2': [71, 73], '3': [72, 74], '4': [73, 75], '5': [74, 76],
    '6': [75, 77], '7': [76, 78], '8': [77, 79], '9': [78, 80], '10': [79, 81]
}
df = pd.DataFrame(example_data)


fixed_columns = ['Patient ID', 'age', 'sex', 'procedure type']


hour_columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']



df_long = pd.melt(
    df, 
    id_vars=fixed_columns, 
    value_vars=hour_columns, 
    var_name='Time since surgery', 
    value_name='Measurement'
)


column_order = ['Time since surgery'] + fixed_columns + ['Measurement']
df_long = df_long[column_order]


df_long = df_long.sort_values(by=['Patient ID', 'Time since surgery'])


df_long = df_long.reset_index(drop=True)


print(df_long)