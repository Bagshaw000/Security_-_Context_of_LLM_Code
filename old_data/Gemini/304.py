import pandas as pd





fixed_columns = ['Patient ID', 'age', 'sex', 'procedure type']



hour_columns = [str(i) for i in range(1, 11)]


df_long = pd.melt(
    df,
    id_vars=fixed_columns,
    value_vars=hour_columns,
    var_name='Time since surgery',
    value_name='Measurement'
)


column_order = ['Time since surgery'] + [col for col in df_long.columns if col != 'Time since surgery']
df_long = df_long[column_order]


df_long['Time since surgery'] = pd.to_numeric(df_long['Time since surgery'])


df_long = df_long.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)