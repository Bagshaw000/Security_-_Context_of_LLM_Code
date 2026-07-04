import pandas as pd




df_long = pd.melt(df, 
                  id_vars=['Patient ID', 'age', 'sex', 'procedure type'], 
                  value_vars=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                  var_name='Time since surgery', 
                  value_name='Reading')


column_order = ['Time since surgery', 'Patient ID', 'age', 'sex', 'procedure type', 'Reading']
df_long = df_long[column_order]


df_long = df_long.sort_values(by=['Patient ID', 'Time since surgery'])

