import pandas as pd


df_melted = pd.melt(df, id_vars=['Patient ID', 'age', 'sex', 'procedure type'], var_name='Time since surgery', value_name='value')
df_final = df_melted.sort_values(['Patient ID', 'Time since surgery'])