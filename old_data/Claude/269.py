import numpy as np
from scipy.spatial import ConvexHull

def convex_hull_4d(points):
    
    hull = ConvexHull(points)
    return hull


points_4d = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
convex_hull = convex_hull_4d(points_4d)