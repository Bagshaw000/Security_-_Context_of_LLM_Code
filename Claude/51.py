Here's an implementation of the convex hull algorithm for 4D points in Python:

import numpy as np
from scipy.spatial import ConvexHull

def convex_hull_4d(points):
    
    hull = ConvexHull(points)
    return points[hull.vertices]


points_4d = np.array([[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [0, 1, 2, 3], [1, 0, 3, 2]])
convex_hull = convex_hull_4d(points_4d)
print(convex_hull)