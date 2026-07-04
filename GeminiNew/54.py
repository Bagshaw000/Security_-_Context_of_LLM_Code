import logging
import unittest
from typing import List, Tuple, Optional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CoinSubsetOptimizer:
    

    def __init__(self):
        pass

    def validate_inputs(self, probabilities: List[float]) -> int:
        
        if not isinstance(probabilities, list):
            raise TypeError("Input 'probabilities' must be a list.")
        
        if not all(isinstance(p, (float, int)) for p in probabilities):
            raise TypeError("All probabilities must be numeric (float or int).")
        
        if any(not (0.0 <= p <= 1.0) for p in probabilities):
            raise ValueError("All probabilities must be between 0 and 1