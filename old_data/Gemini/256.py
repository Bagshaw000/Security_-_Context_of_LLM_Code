import numpy as np
from scipy.spatial import ConvexHull, QhullError
import unittest

def compute_4d_convex_hull(points):
    
    if not isinstance(points, np.ndarray):
        points = np.array(points)

    if points.ndim != 2 or points.shape[1] != 4:
        raise ValueError("Input points must be an (N, 4) array.")

    if points.shape[0] < 5:
        raise ValueError("At least 5 points are required to compute a hull in 4D.")

    try:
        hull = ConvexHull(points)
        return hull
    except QhullError as e:
        
        print(f"Error computing convex hull: {e}")
        return None

class TestConvexHull4D(unittest.TestCase):
    
    def setUp(self):
        
        
        self.points = np.array([
            [0, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1],
            [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 0, 1],
            [0, 0, 1, 1], [1, 1, 1, 0], [1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1],
            [1, 1, 1, 1]
        ])

    def test_hypercube_vertices(self):
        
        points_with_interior = np.vstack([self.points, [0.5, 0.5, 0.5, 0.5]])
        hull = compute_4d_convex_hull(points_with_interior)
        
        
        self.assertEqual(len(hull.vertices), 16)
        
        self.assertNotIn(16, hull.vertices)

    def test_invalid_dimensions(self):
        invalid_points = np.random.rand(10, 3)
        with self.assertRaises(ValueError):
            compute_4d_convex_hull(invalid_points)

    def test_insufficient_points(self):
        few_points = np.random.rand(3, 4)
        with self.assertRaises(ValueError):
            compute_4d_convex_hull(few_points)

if __name__ == "__main__":
    
    print("Generating random 4D points...")
    random_points = np.random.uniform(0, 10, size=(50, 4))
    
    hull = compute_4d_convex_hull(random_points)
    
    if hull:
        print(f"Successfully computed 4D convex hull.")
        print(f"Number of points on the hull: {len(hull.vertices)}")
        print(f"Number of simplices (4D facets): {len(hull.simplices)}")
        print(f"Hull area (3D boundary volume): {hull.area}")
        print(f"Hull volume (4D hypervolume): {hull.volume}")

    print("\nRunning unit tests...")
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestConvexHull4D)
    unittest.TextTestRunner(verbosity=2).run(suite)