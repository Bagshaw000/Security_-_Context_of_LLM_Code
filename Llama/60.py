import pandas as pd
import numpy as np

def transform_df(df):
    df['Time since surgery'] = df.apply(lambda row: (row['age'] - 10)/60, axis=1) 
    hourly_df = df.groupby('Patient ID').apply(lambda x: pd.concat([x.iloc[0]] + [pd.Series(x.iloc[i].to_frame().T.rename(columns={f'hour_{i}': 'Time since surgery'}) for i in range(1, 11)], ignore_index=False), ignore_index=True).reset_index(drop=True)
    return hourly_df

df = pd.DataFrame({
    'Patient ID': np.repeat(range(1, 11), 10),
    'age': np.random.randint(18, 80, 100),
    'sex': np.random.choice(['M', 'F'], 100),
    'procedure type': np.random.choice(['Surgery', 'Procedure'], 100),
    'hour_1': np.random.randint(0, 24, 100),
    'hour_2': np.random.randint(0, 24, 100),
    'hour_3': np.random.randint(0, 24, 100),
    'hour_4': np.random.randint(0, 24, 100),
    'hour_5': np.random.randint(0, 24, 100),
    'hour_6': np.random.randint(0, 24, 100),
    'hour_7': np.random.randint(0, 24, 100),
    'hour_8': np.random.randint(0, 24, 100),
    'hour_9': np.random.randint(0, 24, 100),
    'hour_10': np.random.randint(0, 24, 100)
})

print(transform_df(df))