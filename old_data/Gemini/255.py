import numpy as np
from scipy.spatial import ConvexHull, QhullError
import unittest







class ConvexHull4DService:
    
    def __init__(self, points):
        
        self.points = np.asanyarray(points)
        self.hull = None
        self._validate_input()

    def _validate_input(self):
        if self.points.ndim != 2 or self.points.shape[1] != 4:
            raise ValueError("Input points must be in 4D format: (N, 4).")
        if len(self.points) < 5:
            raise ValueError("A 4D convex hull requires at least 5 points to form a simplex.")

    def compute(self):
        """
        Computes the convex hull using the Quick