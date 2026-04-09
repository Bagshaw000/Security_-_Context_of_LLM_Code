import pandas as pd


fixed_cols = ['Patient ID', 'age', 'sex', 'procedure type']


hour_cols = [c for c in df.columns if c not in fixed_cols]


df_long = df.melt(
    id_vars=fixed_cols,
    value_vars=hour_cols,
    var_name='Time since surgery',
    value_name='Value'
)


cols = ['Time since surgery'] + [c for c in df_long.columns if c != 'Time since surgery']
df_long = df_long[cols]


df_long['Time since surgery'] = pd.to_numeric(df_long['Time since surgery'])


df_long = df_long.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)