



import pandas as pd




invariables = ['Patient ID', 'age', 'sex', 'procedure type']




variables = ['Hour 1', 'Hour 2', 'Hour 3', 'Hour 4', 'Hour 5', 'Hour 6', 'Hour 7', 'Hour 8', 'Hour 9', 'Hour 10']




data = {
    'Patient ID': [1001], 
    'age': [65], 
    'sex': ['M'], 
    'procedure type': ['Orthopedic'],
    'Hour 1': [98.2], 'Hour 2': [98.4], 'Hour 3': [98.6], 'Hour 4': [98.5], 'Hour 5': [98.3],
    'Hour 6': [98.2], 'Hour 7': [98.1], 'Hour 8': [98.0], 'Hour 9': [97.9], 'Hour 10': [98.1]
}
wide_table = pd.DataFrame(data)






long_table = wide_table.melt(
    id_vars=invariables,
    value_vars=variables,
    var_name='Time since surgery',
    value_name='Recovery Measurement'
)




long_table = long_table.sort_values(by=['Patient ID', 'Time since surgery'])




print(long_table)