import pandas as pd
import numpy as np
from typing import List

def sanitize_and_validate_dataframe(df: pd.DataFrame, required_fixed_cols: List[str], observation_cols: List[str]) -> pd.DataFrame:
    
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]

    
    all_required = required_fixed_cols + observation_cols
    missing_cols = [col for col in all_required if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Input DataFrame is missing required columns: {missing_cols}")

    
    
    if df['Patient ID'].isnull().any():
        df = df.dropna(subset=['Patient ID'])

    
    df['age'] = pd.to_numeric(df['age'], errors='coerce')

    return df

def transform_patient_data_wide_to_long(df: pd.DataFrame) -> pd.DataFrame:
    
    fixed_vars = ['Patient ID', 'age', 'sex', 'procedure type']
    obs_vars = [str(i) for i in range(1, 11)]

    
    clean_df = sanitize_and_validate_dataframe(df, fixed_vars, obs_vars)

    
    
    long_df = pd.melt(
        clean_df,
        id_vars=fixed_vars,
        value_vars=obs_vars,
        var_name='Time since surgery',
        value_name='observation_value'
    )

    
    long_df['Time since surgery'] = pd.to_numeric(long_df['Time since surgery'], errors='coerce')

    
    long_df['observation_value'] = pd.to_numeric(long_df['observation_value'], errors='coerce')

    
    column_order = ['Time since surgery'] + fixed_vars + ['observation_value']
    long_df = long_df[column_order]

    
    long_df = long_df.sort_values(by=['Patient ID', 'Time since surgery']).reset_index(drop=True)

    return long_df



import unittest

class TestPatientDataTransformation(unittest.TestCase):
    def setUp(self):
        
        data = {
            'Patient ID': ['P001', 'P002'],
            'age': [45, 60],
            'sex': ['M', 'F'],
            'procedure type': ['Appendectomy', 'Cholecystectomy'],
            '1': [120, 110], '2': [122, 112], '3': [121, 115], 
            '4': [125, 118], '5': [130, 120], '6': [128, 122], 
            '7': [126, 121], '8': [124, 119], '9': [122, 117], 
            '10': [120, 115]
        }
        self.valid_df = pd.DataFrame(data)

    def test_transformation_output_dimensions(self):
        
        result = transform_patient_data_wide_to_long(self.valid_df)
        self.assertEqual(len(result), 20)
        self.assertEqual(result.columns[0], 'Time since surgery')

    def test_column_broadcasting(self):
        
        result = transform_patient_data_wide_to_long(self.valid_df)
        p1_data = result[result['Patient ID'] == 'P001']
        self.assertTrue((p1_data['age'] == 45).all())
        self.assertTrue((p1_data['sex'] == 'M').all())

    def test_missing_required_column(self):
        
        invalid_df = self.valid_df.drop(columns=['10'])
        with self.assertRaises(ValueError):
            transform_patient_data_wide_to_long(invalid_df)

    def test_malformed_patient_id(self):
        
        df_with_nan = pd.concat([self.valid_df, pd.DataFrame([{'Patient ID': None, 'age': 30}])], ignore_index=True)
        result = transform_patient_data_wide_to_long(df_with_nan)
        
        self.assertEqual(len(result), 20)

if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPatientDataTransformation)
    unittest.TextTestRunner(verbosity=1).run(suite)