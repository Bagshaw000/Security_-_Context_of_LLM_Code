import pandas as pd

df = pd.DataFrame({'Patient ID': [1, 1, 1, 2, 2, 2], 
                   'age': [40, 40, 40, 50, 50, 50],
                   'sex': ['M', 'M', 'M', 'F', 'F', 'F'],
                   'procedure type': ['surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery'],
                   'hour 1': [100, 150, 120, 90, 110, 100],
                   'hour 2': [95, 145, 115, 85, 105, 95],
                   'hour 3': [90, 140, 110, 80, 100, 90],
                   'hour 4': [85, 135, 105, 75, 95, 85],
                   'hour 5': [80, 130, 100, 70, 90, 80],
                   'hour 6': [75, 125, 95, 65, 85, 75],
                   'hour 7': [70, 120, 90, 60, 80, 70],
                   'hour 8': [65, 115, 85, 55, 75, 65],
                   'hour 9': [60, 110, 80, 50, 70, 60],
                   'hour 10': [55, 105, 75, 45, 65, 55]})


melted_df = pd.melt(df, id_vars=['Patient ID', 'age', 'sex', 'procedure type'], var_name='Time since surgery', value_name='Value')


melted_df['Time since surgery'] = melted_df['Time since surgery'].str.extract('(\d+)', expand=False)
melted_df['Time since surgery'] = melted_df['Time since surgery'].astype(int)


melted_df = melted_df.sort_values(['Patient ID', 'Time since surgery'])


melted_df = melted_df.reset_index(drop=True)