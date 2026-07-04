import pandas as pd


df_long = pd.melt(df, id_vars=['Patient ID', 'age', 'sex', 'procedure type'], var_name='Time since surgery', value_name='Value')