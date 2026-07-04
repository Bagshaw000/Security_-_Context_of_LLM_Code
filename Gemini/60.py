import pandas as pd

id_vars = ['Patient ID', 'age', 'sex', 'procedure type']

df_long = df.melt(
    id_vars=id_vars,
    var_name='Time since surgery',
    value_name='Value'
)

df_long['Time since surgery'] = pd.to_numeric(df_long['Time since surgery'])

column_order = ['Time since surgery'] + id_vars + ['Value']
df_long = df_long[column_order]

df_long = df_long.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)