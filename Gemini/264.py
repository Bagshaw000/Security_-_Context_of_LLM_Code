import numpy as np
from scipy.spatial import ConvexHull
from typing import Dict, Any, Optional, Union

class ConvexHull4D:
    

    def __init__(self, points: Union[np.ndarray, list]):
        
        self.points = self._initialize_points(points)
        self._validate_input()
        self.hull: Optional[ConvexHull] = None

    def _initialize_points(self, points: Any) -> np.ndarray:
        
        return np.asarray(points)

    def _validate_input(self) -> None:
        """
        Validates that the