import pandas as pd

def transform_dataframe(df):
    
    melted_df = df.melt(id_vars=['Patient ID', 'age', 'sex', 'procedure type'], 
                        value_vars=[str(i) for i in range(1, 11)], 
                        var_name='Hour', 
                        value_name='Value')
    
    
    melted_df['Time since surgery'] = melted_df['Hour'].astype(int)
    
    
    final_df = melted_df.drop(columns=['Hour']).dropna()
    
    return final_df.reset_index(drop=True)




















