import pandas as pd


id_vars = ['Patient ID', 'age', 'sex', 'procedure type']


hour_vars = [col for col in df.columns if col not in id_vars]


df_long = pd.melt(
    df,
    id_vars=id_vars,
    value_vars=hour_vars,
    var_name='Time since surgery',
    value_name='Value'
)


column_order = ['Time since surgery'] + [col for col in df_long.columns if col != 'Time since surgery']
df_transformed = df_long[column_order]


df_transformed = df_transformed.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)