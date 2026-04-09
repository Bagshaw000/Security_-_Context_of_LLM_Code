import pandas as pd


data = {
    'Patient ID': [101, 102],
    'age': [45, 62],
    'sex': ['M', 'F'],
    'procedure type': ['Appendectomy', 'Cholecystectomy'],
    '1': [80, 85], '2': [82, 84], '3': [79, 88], '4': [81, 86], '5': [80, 87],
    '6': [82, 85], '7': [83, 84], '8': [81, 86], '9': [80, 85], '10': [79, 87]
}
df = pd.DataFrame(data)


id_vars = ['Patient ID', 'age', 'sex', 'procedure type']


hour_columns = [str(i) for i in range(1, 11)]


df_reorganized = pd.melt(
    df, 
    id_vars=id_vars, 
    value_vars=hour_columns, 
    var_name='Time since surgery', 
    value_name='Value'
)


df_reorganized['Time since surgery'] = pd.to_numeric(df_reorganized['Time since surgery'])


cols = ['Time since surgery'] + id_vars + ['Value']
df_reorganized = df_reorganized[cols]


df_reorganized = df_reorganized.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)


print(df_reorganized)