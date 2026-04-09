import pandas as pd


fixed_vars = ['Patient ID', 'age', 'sex', 'procedure type']
hour_vars = [col for col in df.columns if col not in fixed_vars]


df_long = df.melt(
    id_vars=fixed_vars,
    value_vars=hour_vars,
    var_name='Time since surgery',
    value_name='Value'
)


new_column_order = ['Time since surgery'] + fixed_vars + ['Value']
df_long = df_long[new_column_order]


df_long = df_long.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)