import pandas as pd

def transform_df(df):
    df['Time since surgery'] = 1 + (df.iloc[:,2:] - df.iloc[:,0:2]).mean(axis=1)
    df[['hour1','hour2','hour3','hour4','hour5','hour6','hour7','hour8','hour9','hour10']] = df.iloc[:,2:].sum(axis=0)
    new_df = pd.DataFrame(index=df.index)
    for i in range(len(df)):
        row = {'Patient ID': df.loc[i,'Patient ID'],
               'age': df.loc[i,'age'],
               'sex': df.loc[i,'sex'],
               'procedure type': df.loc[i,'procedure type']}
        for j in range(10):
            if j<9:
                row[f'hour{j+1}'] = df.loc[i,j+2]
            else:
                row[f'hour{j+1}'] = 0
        new_df.loc[new_df.index[i],:] = row
    return new_df[['Patient ID','age','sex', 'procedure type','Time since surgery']+['hour'+str(i) for i in range(1,11)]]

df = pd.DataFrame({
   'Patient ID': [1,2,3],
   'age': [25,30,35],
   'sex': ['M','F','M'],
   'procedure type': ['surgery','exam','checkup'],
   'hour1': [5,10,15],
   'hour2': [20,12,18],
   'hour3': [25,11,22],
   'hour4': [27,9,19],
   'hour5': [30,8,17],
   'hour6': [32,7,16],
   'hour7': [33,6,15],
   'hour8': [34,5,14],
   'hour9': [35,4,13],
   'hour10': [36,3,12]
})

print(transform_df(df))