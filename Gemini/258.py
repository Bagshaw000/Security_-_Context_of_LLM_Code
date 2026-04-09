import numpy as np

class ConvexHull4D:
    

    def __init__(self, points):
        
        self.points = np.array(points)
        if self.points.shape[1] != 4:
            raise ValueError("Input points must be 4-dimensional.")
        self.num_points = len(self.points)

    def _get_normal(self, facet_indices):
        
        pts = self.points[list(facet_indices)]
        v1 = pts[1] - pts[0]
        v2 = pts[2] - pts[0]
        v3 = pts[3] - pts[0]

        
        mat = np.vstack([v1, v2, v3])
        
        normal = np.array([
            np.linalg.det(mat[:,