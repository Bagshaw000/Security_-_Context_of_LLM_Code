import pandas as pd


id_vars = ['Patient ID', 'age', 'sex', 'procedure type']



hour_vars = [col for col in df.columns if str(col) in [str(i) for i in range(1, 11)]]


df_long = df.melt(
    id_vars=id_vars,
    value_vars=hour_vars,
    var_name='Time since surgery',
    value_name='Measurement'
)


df_long['Time since surgery'] = pd.to_numeric(df_long['Time since surgery'])



ordered_cols = ['Time since surgery'] + id_vars + ['Measurement']
df_long = df_long[ordered_cols]


df_long = df_long.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)

