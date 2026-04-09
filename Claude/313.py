import pandas as pd

df = pd.DataFrame({'Patient ID': [1, 1, 1, 2, 2, 2], 
                   'age': [45, 45, 45, 32, 32, 32],
                   'sex': ['M', 'M', 'M', 'F', 'F', 'F'],
                   'procedure type': ['surgery', 'surgery', 'surgery', 'surgery', 'surgery', 'surgery'],
                   'hour 1': [80, 85, 90, 75, 80, 85],
                   'hour 2': [75, 80, 85, 70, 75, 80],
                   'hour 3': [70, 75, 80, 65, 70, 75],
                   'hour 4': [65, 70, 75, 60, 65, 70],
                   'hour 5': [60, 65, 70, 55, 60, 65],
                   'hour 6': [55, 60, 65, 50, 55, 60],
                   'hour 7': [50, 55, 60, 45, 50, 55],
                   'hour 8': [45, 50, 55, 40, 45, 50],
                   'hour 9': [40, 45, 50, 35, 40, 45],
                   'hour 10': [35, 40, 45, 30, 35, 40]})

new_df = pd.melt(df, id_vars=['Patient ID', 'age', 'sex', 'procedure type'], 
                 var_name='Time since surgery', value_name='Measurement')
new_df['Time since surgery'] = new_df['Time since surgery'].str.replace('hour ', '')
new_df['Time since surgery'] = new_df['Time since surgery'].astype(int)