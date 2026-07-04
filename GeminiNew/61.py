import pandas as pd
import numpy as np
from typing import List, Final

class ClinicalDataPipeline:
    

    REQUIRED_METADATA: Final[List[str]] = [
        "Patient ID",
        "age",
        "sex",
        "procedure type"
    ]

    def __init__(self, observation_count: int = 10):
        
        self.observation_cols = [str(i) for i in range(1, observation_count + 1)]
        self.expected_columns = self.REQUIRED_METADATA + self.observation_cols

    def _validate_input_schema(self, df: pd.DataFrame) -> None:
        
        if df is None or df.empty:
            raise ValueError("Input dataset is empty or null.")

        actual_cols = set(df.columns)
        required_cols = set(self.expected_columns)

        if not required_cols.issubset(actual_cols):
            missing = required_cols - actual_cols
            raise ValueError(f"Schema validation failed. Missing columns: {missing}")

    def _apply_memory_optimization(self, df: pd.DataFrame) -> pd.DataFrame:
        
        
        for col in ["sex", "procedure type"]:
            df[col] = df[col].astype("category")
        
        
        if "age" in df.columns:
            df["age"] = pd.to_numeric(df["age"], errors="coerce").astype(np.float32)
            
        return df

    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        
        
        self._validate_input_schema(df)

        
        working_df = df[self.expected_columns].copy()
        working_df = self._apply_memory_optimization(working_df)

        try:
            
            
            tidy_df = pd.melt(
                working_df,
                id_vars=self.REQUIRED_METADATA,
                value_vars=self.observation_cols,
                var_name="Time since surgery",
                value_name="Observation Value"
            )

            
            
            tidy_df["Time since surgery"] = pd.to_numeric(
                tidy_df["Time since surgery"], 
                errors="coerce"
            ).astype(np.int32)

            
            tidy_df["Observation Value"] = pd.to_numeric(
                tidy_df["Observation Value"], 
                errors="coerce"
            )

            
            column_order = ["Time since surgery"] + self.REQUIRED_METADATA + ["Observation Value"]
            tidy_df = tidy_df[column_order]

            
            
            tidy_df.dropna(subset=["Patient ID", "Time since surgery"], inplace=True)

            return tidy_df.reset_index(drop=True)

        except Exception as e:
            
            raise RuntimeError(f"Critical failure during data normalization: {str(e)}")

def process_clinical_dataset(input_dataframe: pd.DataFrame) -> pd.DataFrame:
    
    pipeline = ClinicalDataPipeline(observation_count=10)
    return pipeline.normalize(input_dataframe)