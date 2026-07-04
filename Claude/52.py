import numpy as np
from scipy.spatial import ConvexHull

def convex_hull_4d(points):
    hull = ConvexHull(points)
    return hull.vertices


points = np.array([[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7], [5, 6, 7, 8], [6, 7, 8, 9]])
convex_hull_indices = convex_hull_4d(points)
print(convex_hull_indices)