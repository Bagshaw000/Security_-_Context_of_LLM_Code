import pandas as pd

df = pd.DataFrame({'Patient ID': [1, 2, 3, 4, 5],
                   'age': [45, 52, 38, 64, 29],
                   'sex': ['M', 'F', 'M', 'F', 'M'],
                   'procedure type': ['A', 'B', 'A', 'C', 'B'],
                   'Hour 1': [80, 90, 85, 92, 88],
                   'Hour 2': [82, 92, 87, 94, 90],
                   'Hour 3': [84, 94, 89, 96, 92],
                   'Hour 4': [86, 96, 91, 98, 94],
                   'Hour 5': [88, 98, 93, 100, 96],
                   'Hour 6': [90, 100, 95, 102, 98],
                   'Hour 7': [92, 102, 97, 104, 100],
                   'Hour 8': [94, 104, 99, 106, 102],
                   'Hour 9': [96, 106, 101, 108, 104],
                   'Hour 10': [98, 108, 103, 110, 106]})

new_df = pd.DataFrame()
for i in range(1, 11):
    temp_df = df.copy()
    temp_df['Time since surgery'] = f'Hour {i}'
    for col in [f'Hour {j}' for j in range(1, 11)]:
        temp_df[col] = temp_df[col].shift(i-1)
    new_df = pd.concat([new_df, temp_df], ignore_index=True)