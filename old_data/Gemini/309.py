import pandas as pd

fixed_columns = ['Patient ID', 'age', 'sex', 'procedure type']
hour_columns = [col for col in df.columns if col not in fixed_columns]

df_long = pd.melt(
    df, 
    id_vars=fixed_columns, 
    value_vars=hour_columns, 
    var_name='Time since surgery', 
    value_name='Measurement'
)

column_order = ['Time since surgery'] + fixed_columns + ['Measurement']
df_final = df_long[column_order]

df_final['Time since surgery'] = pd.to_numeric(df_final['Time since surgery'])
df_final = df_final.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)