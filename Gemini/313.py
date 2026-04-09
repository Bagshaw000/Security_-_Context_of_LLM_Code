import pandas as pd


fixed_columns = ['Patient ID', 'age', 'sex', 'procedure type']



hour_columns = [col for col in df.columns if col not in fixed_columns]



df_reorganized = pd.melt(df, 
                         id_vars=fixed_columns, 
                         value_vars=hour_columns, 
                         var_name='Time since surgery', 
                         value_name='Value')


all_columns = df_reorganized.columns.tolist()
all_columns.insert(0, all_columns.pop(all_columns.index('Time since surgery')))
df_reorganized = df_reorganized[all_columns]


print(df_reorganized)