import pandas as pd





fixed_details = ['Patient ID', 'age', 'sex', 'procedure type']


hourly_columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']


df_long = pd.melt(
    df, 
    id_vars=fixed_details, 
    value_vars=hourly_columns, 
    var_name='Time since surgery', 
    value_name='Value'
)


new_column_order = ['Time since surgery', 'Patient ID', 'age', 'sex', 'procedure type', 'Value']
df_long = df_long[new_column_order]


df_long = df_long.sort_values(by=['Patient ID', 'Time since surgery'])


df_long = df_long.reset_index(drop=True)

