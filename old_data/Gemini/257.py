import numpy as np
from scipy.spatial import ConvexHull
import unittest

def compute_4d_convex_hull(points):
    
    
    points = np.asarray(points)
    
    
    if points.ndim != 2 or points.shape[1] != 4:
        raise ValueError("Input points must have shape (N, 4).")
    
    
    if points.shape[0] < 5:
        raise ValueError("At least 5 points are required to compute a 4D convex hull.")
        
    try:
        
        hull = ConvexHull(points)
        return hull
    except Exception as e:
        
        raise RuntimeError(f"Failed to compute convex hull: {e}")

class TestConvexHull4D(unittest.TestCase):
    
    
    def setUp(self):
        
        self.hypercube_points = np.array([
            [i, j, k, l] 
            for i in [0, 1] 
            for j in [0, 1] 
            for k in [0, 1] 
            for l in [0, 1]
        ])

    def test_hypercube_volume(self):
        
        hull = compute_4d_convex_hull(self.hypercube_points)
        self.assertAlmostEqual(hull.volume, 1.0, places=5)

    def test_hypercube_vertices(self):
        
        hull = compute_4d_convex_hull(self.hypercube_points)
        self.assertEqual(len(hull.vertices), 16)

    def test_internal_points_exclusion(self):
        
        internal_point = np.array([[0.5, 0.5, 0.5, 0.5]])
        test_points = np.vstack([self.hypercube_points, internal_point])
        hull = compute_4d_convex_hull(test_points)
        
        self.assertEqual(len(hull.vertices), 16)

    def test_invalid_dimensions(self):
        
        points_3d = np.random.rand(10, 3)
        with self.assertRaises(ValueError):
            compute_4d_convex_hull(points_3d)

if __name__ == "__main__":
    
    print("Generating random 4D point cloud...")
    np.random.seed(42)
    random_data = np.random.rand(30, 4)
    
    try:
        result = compute_4d_convex_hull(random_data)
        print("4D Convex Hull successfully calculated.")
        print(f"Number of points on the hull: {len(result.vertices)}")
        print(f"Number of facets (4D simplices): {len(result.simplices)}")
        print(f"Hypervolume: {result.volume:.4f}")
    except Exception as err:
        print(f"Error: {err}")

    
    print("\nExecuting Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConvexHull4D)
    unittest.TextTestRunner(verbosity=2).run(suite)