import logging
import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class TransformationConfig:
    
    patient_id_col: str = 'Patient ID'
    age_col: str = 'age'
    sex_col: str = 'sex'
    procedure_col: str = 'procedure_type'
    hour_prefix: str = 'hour_'
    num_hours: int = 10
    time_col_name: str = 'Time since surgery (hours)'
    measurement_col_name: str = 'measurement_value'


class DataFrameTransformationError(Exception):
    
    pass


class PatientDataTransformer:
    
    
    def __init__(self, config: Optional[TransformationConfig] = None) -> None:
        
        self.config = config or TransformationConfig()
        logger.info(f"PatientDataTransformer initialized with config: {self.config}")
    
    def validate_input_dataframe(self, df: pd.DataFrame) -> None:
        
        if df is None:
            raise DataFrameTransformationError("Input DataFrame cannot be None")
        
        if not isinstance(df, pd.DataFrame):
            raise DataFrameTransformationError(
                f"Expected pandas DataFrame, got {type(df).__name__}"
            )
        
        if df.empty:
            logger.warning("Input DataFrame is empty")
            return
        
        required_columns = [
            self.config.patient_id_col,
            self.config.age_col,
            self.config.sex_col,
            self.config.procedure_col
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise DataFrameTransformationError(
                f"Missing required columns: {missing_columns}"
            )
        
        hour_columns = [
            f"{self.config.hour_prefix}{i}" for i in range(1, self.config.num_hours + 1)
        ]
        missing_hour_columns = [col for col in hour_columns if col not in df.columns]
        if missing_hour_columns:
            raise DataFrameTransformationError(
                f"Missing hour columns: {missing_hour_columns}"
            )
        
        if df[self.config.patient_id_col].isna().any():
            raise DataFrameTransformationError(
                f"'{self.config.patient_id_col}' column contains null values"
            )
        
        if df[self.config.age_col].isna().any():
            raise DataFrameTransformationError(
                f"'{self.config.age_col}' column contains null values"
            )
        
        if df[self.config.sex_col].isna().any():
            raise DataFrameTransformationError(
                f"'{self.config.sex_col}' column contains null values"
            )
        
        if df[self.config.procedure_col].isna().any():
            raise DataFrameTransformationError(
                f"'{self.config.procedure_col}' column contains null values"
            )
        
        try:
            pd.to_numeric(df[self.config.age_col], errors='coerce')
            if df[self.config.age_col].dtype not in [np.int64, np.int32, np.float64, np.float32]:
                logger.warning(f"'{self.config.age_col}' may not be numeric type")
        except Exception as e:
            raise DataFrameTransformationError(
                f"'{self.config.age_col}' contains non-numeric values: {str(e)}"
            )
        
        hour_columns = [
            f"{self.config.hour_prefix}{i}" for i in range(1, self.config.num_hours + 1)
        ]
        for col in hour_columns:
            if col in df.columns and df[col].dtype == 'object':
                try:
                    pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    raise DataFrameTransformationError(
                        f"Column '{col}' contains non-numeric values: {str(e)}"
                    )
        
        logger.info(f"Input validation passed for DataFrame with {len(df)} rows")
    
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        
        try:
            self.validate_input_dataframe(df)
            
            if df.empty:
                logger.info("Returning empty DataFrame for empty input")
                return self._create_empty_result_dataframe()
            
            hour_columns = [
                f"{self.config.hour_prefix}{i}" for i in range(1, self.config.num_hours + 1)
            ]
            
            id_vars = [
                self.config.patient_id_col,
                self.config.age_col,
                self.config.sex_col,
                self.config.procedure_col
            ]
            
            melted_df = pd.melt(
                df,
                id_vars=id_vars,
                value_vars=hour_columns,
                var_name='hour_column',
                value_name=self.config.measurement_col_name
            )
            
            melted_df[self.config.time_col_name] = melted_df['hour_column'].str.extract(
                r'(\d+)'
            ).astype(int)
            
            melted_df = melted_df.drop(columns=['hour_column'])
            
            column_order = [
                self.config.patient_id_col,
                self.config.time_col_name,
                self.config.age_col,
                self.config.sex_col,
                self.config.procedure_col,
                self.config.measurement_col_name
            ]
            
            melted_df = melted_df[column_order]
            
            melted_df = melted_df.reset_index(drop=True)
            
            logger.info(
                f"Transformation completed: {len(df)} input rows -> {len(melted_df)} output rows"
            )
            
            return melted_df
            
        except DataFrameTransformationError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error during transformation: {str(e)}")
            raise DataFrameTransformationError(
                f"Transformation failed: {str(e)}"
            )
    
    def _create_empty_result_dataframe(self) -> pd.DataFrame:
        
        columns = [
            self.config.patient_id_col,
            self.config.time_col_name,
            self.config.age_col,
            self.config.sex_col,
            self.config.procedure_col,
            self.config.measurement_col_name
        ]
        return pd.DataFrame(columns=columns)


def create_sample_data() -> pd.DataFrame:
    
    data = {
        'Patient ID': ['P001', 'P002', 'P003'],
        'age': [45, 67, 52],
        'sex': ['M', 'F', 'M'],
        'procedure_type': ['Surgery A', 'Surgery B', 'Surgery A'],
        'hour_1': [100.5, 102.3, 98.7],
        'hour_2': [101.2, 103.1, 99.2],
        'hour_3': [99.8, 101.5, 100.1],
        'hour_4': [102.3, 104.2, 99.5],
        'hour_5': [103.1, 105.0, 101.2],
        'hour_6': [101.5, 103.7, 100.8],
        'hour_7': [100.2, 102.9, 99.3],
        'hour_8': [99.7, 101.4, 98.9],
        'hour_9': [102.1, 104.6, 101.5],
        'hour_10': [100.9, 103.2, 100.2]
    }
    return pd.DataFrame(data)


def run_unit_tests() -> None:
    
    
    logger.info("Starting unit tests...")
    
    transformer = PatientDataTransformer()
    
    logger.info("Test 1: Valid input DataFrame transformation")
    try:
        sample_df = create_sample_data()
        result = transformer.transform(sample_df)
        assert len(result) == 30, f"Expected 30 rows, got {len(result)}"
        assert len(result.columns) == 6, f"Expected 6 columns, got {len(result.columns)}"
        assert all(result['Time since surgery (hours)'].isin(range(1, 11))), \
            "Time values should be 1-10"
        logger.info("✓ Test 1 passed")
    except Exception as e:
        logger.error(f"✗ Test 1 failed: {str(e)}")
    
    logger.info("Test 2: Empty DataFrame")
    try:
        empty_df = pd.DataFrame(columns=[
            'Patient ID', 'age', 'sex', 'procedure_type',
            'hour_1', 'hour_2', 'hour_3', 'hour_4', 'hour_5',
            'hour_6', 'hour_7', 'hour_8', 'hour_9', 'hour_10'
        ])
        result = transformer.transform(empty_df)
        assert result.empty, "Result should be empty for empty input"
        logger.info("✓ Test 2 passed")
    except Exception as e:
        logger.error(f"✗ Test 2 failed: {str(e)}")
    
    logger.info("Test 3: Missing required column")
    try:
        invalid_df = create_sample_data().drop('age', axis=1)
        transformer.transform(invalid_df)
        logger.error("✗ Test 3 failed: Should have raised DataFrameTransformationError")
    except DataFrameTransformationError:
        logger.info("✓ Test 3 passed")
    except Exception as e:
        logger.error(f"✗ Test 3 failed with unexpected error: {str(e)}")
    
    logger.info("Test 4: Missing hour column")
    try:
        invalid_df = create_sample_data().drop('hour_5', axis=1)
        transformer.transform(invalid_df)
        logger.error("✗ Test 4 failed: Should have raised DataFrameTransformationError")
    except DataFrameTransformationError:
        logger.info("✓ Test 4 passed")
    except Exception as e:
        logger.error(f"✗ Test 4 failed with unexpected error: {str(e)}")
    
    logger.info("Test 5: Null values in invariant columns")
    try:
        invalid_df = create_sample_data()
        invalid_df.loc[0, 'age'] = None
        transformer.transform(invalid_df)
        logger.error("✗ Test 5 failed: Should have raised DataFrameTransformationError")
    except DataFrameTransformationError:
        logger.info("✓ Test 5 passed")
    except Exception as e:
        logger.error(f"✗ Test 5 failed with unexpected error: {str(e)}")
    
    logger.info("Test 6: Non-numeric age column")
    try:
        invalid_df = create_sample_data()
        invalid_df.loc[0, 'age'] = 'invalid'
        transformer.transform(invalid_df)
        logger.error("✗ Test 6 failed: Should have raised DataFrameTransformationError")
    except DataFrameTransformationError:
        logger.info("✓ Test 6 passed")
    except Exception as e:
        logger.error(f"✗ Test 6 failed with unexpected error: {str(e)}")
    
    logger.info("Test 7: None input")
    try:
        transformer.transform(None)
        logger.error("✗ Test 7 failed: Should have raised DataFrameTransformationError")
    except DataFrameTransformationError:
        logger.info("✓ Test 7 passed")
    except Exception as e:
        logger.error(f"✗ Test 7 failed with unexpected error: {str(e)}")
    
    logger.info("Test 8: Non-DataFrame input")
    try:
        transformer.transform([1, 2, 3])
        logger.error("✗ Test 8 failed: Should have raised DataFrameTransformationError")
    except DataFrameTransformationError:
        logger.info("✓ Test 8 passed")
    except Exception as e:
        logger.error(f"✗ Test 8 failed with unexpected error: {str(e)}")
    
    logger.info("Test 9: Null Patient ID")
    try:
        invalid_df = create_sample_data()
        invalid_df.loc[0, 'Patient ID'] = None
        transformer.transform(invalid_df)
        logger.error("✗ Test 9 failed: Should have raised DataFrameTransformationError")
    except DataFrameTransformationError:
        logger.info("✓ Test 9 passed")
    except Exception as e:
        logger.error(f"✗ Test 9 failed with unexpected error: {str(e)}")
    
    logger.info("Test 10: Column order verification")
    try:
        sample_df = create_sample_data()
        result = transformer.transform(sample_df)
        expected_order = [
            'Patient ID',
            'Time since surgery (hours)',
            'age',
            'sex',
            'procedure_type',
            'measurement_value'
        ]
        assert list(result.columns) == expected_order, \
            f"Column order mismatch. Expected {expected_order}, got {list(result.columns)}"
        logger.info("✓ Test 10 passed")
    except Exception as e:
        logger.error(f"✗ Test 10 failed: {str(e)}")
    
    logger.info("Unit tests completed")


def demonstrate_transformation() -> None:
    
    
    logger.info("=" * 80)
    logger.info("DEMONSTRATION: Patient Data Time-Series Transformation")
    logger.info("=" * 80)
    
    sample_df = create_sample_data()
    
    logger.info("\nINPUT DATA (Denormalized):")
    logger.info(f"\nShape: {sample_df.shape}")
    logger.info(f"\nFirst few rows:\n{sample_df.iloc[:, :8]}")
    
    transformer = PatientDataTransformer()
    result_df = transformer.transform(sample