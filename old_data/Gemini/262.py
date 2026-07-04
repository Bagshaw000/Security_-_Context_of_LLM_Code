import numpy as np
from itertools import combinations
from typing import List, Tuple, Set

class Facet4D:
    
    def __init__(self, indices: Tuple[int, ...], points: np.ndarray, internal_point: np.ndarray):
        self.indices = tuple(sorted(indices))
        self.vertices = points[list(self.indices)]
        
        
        
        
        edge_matrix = self.vertices[1:] - self.vertices[0]
        _, _, vh = np.linalg.svd(edge_matrix)
        self.normal = vh[-1]
        
        
        
        
        direction_vec = self.vertices[0] - internal_point
        if np.dot(self.normal, direction_vec) < 0:
            self