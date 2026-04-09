import pandas as pd


id_vars = ['Patient ID', 'age', 'sex', 'procedure type']
hour_vars = [col for col in df.columns if col not in id_vars]


df_transformed = df.melt(
    id_vars=id_vars, 
    value_vars=hour_vars, 
    var_name='Time since surgery', 
    value_name='Measurement'
)


column_order = ['Time since surgery'] + id_vars + ['Measurement']
df_transformed = df_transformed[column_order]


df_transformed['Time since surgery'] = pd.to_numeric(df_transformed['Time since surgery'])


df_transformed = df_transformed.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)