import numpy as np
from scipy.spatial import ConvexHull, QhullError

class ConvexHull4DSolver:
    

    def __init__(self, points):
        
        self.points = np.asarray(points)
        self.hull = None
        self._validate_input()

    def _validate_input(self):
        
        if self.points.ndim != 2 or self.points.shape[1] != 4:
            raise ValueError("Input points must have shape (N, 4).")
        if self.points.shape[0] < 5:
            
            raise ValueError("At least 5 points are required to compute a 4D convex hull.")

    def compute(self):
        
        try:
            
            self.hull = ConvexHull(self.points)
            return self.hull
        except QhullError as e:
            raise RuntimeError(f"Qhull failed to compute the 4D hull: {e}")

    def get_metrics(self):
        
        if self.hull is None:
            self.compute()
            
        return {
            "hypervolume": self.hull.volume,  
            "surface_area": self.hull.area,   
            "facets": self.hull.simplices,    
            "vertices": self.hull.vertices    
        }

    def get_hyperplane_equations(self):
        
        if self.hull is None:
            self.compute()
        return self.hull.equations

def run_unit_test():
    
    import itertools
    
    
    hypercube_points = np.array(list(itertools.product([0, 1], repeat=4)))
    
    
    points = np.vstack([hypercube_points, [0.5, 0.5, 0.5, 0.5]])
    
    solver = ConvexHull4DSolver(points)
    metrics = solver.get_metrics()
    
    
    assert len(metrics["vertices"]) == 16, "Hull should contain 16 vertices"
    assert np.isclose(metrics["hypervolume"], 1.0), "Hypervolume should be 1.0"