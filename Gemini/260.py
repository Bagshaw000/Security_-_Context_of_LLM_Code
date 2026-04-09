import numpy as np
from itertools import combinations

class Facet4D:
    
    def __init__(self, indices, points, internal_point):
        self.indices = tuple(sorted(indices))
        self.points_subset = points[list(self.indices)]
        self.normal, self.offset = self._compute_hyperplane(internal_point)

    def _compute_hyperplane(self, internal_point):
        
        
        v1 = self.points_subset[1] - self.points_subset[0]
        v2 = self.points_subset[2] - self.points_subset[0]
        v3 = self.points_subset[3] - self.points_subset[0]
        
        
        mat = np.array([v1, v2, v3])
        
        
        n = np.array([
            np.linalg.det(mat[:, [1, 2