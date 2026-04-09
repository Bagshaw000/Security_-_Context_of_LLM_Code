import pandas as pd





hour_columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']



df_long = df.melt(
    id_vars=['Patient ID', 'age', 'sex', 'procedure type'],
    value_vars=hour_columns,
    var_name='Time since surgery',
    value_name='Measurement'
)


df_long['Time since surgery'] = pd.to_numeric(df_long['Time since surgery'])


other_columns = [col for col in df_long.columns if col != 'Time since surgery']
df_long = df_long[['Time since surgery'] + other_columns]


df_long = df_long.sort_values(by=['Patient ID', 'Time since surgery'])


print(df_long.head())