import numpy as np
from scipy.spatial import ConvexHull

def convex_hull_4d(points):
    hull = ConvexHull(points)
    return hull.vertices


points_4d = np.random.rand(10, 4)
convex_hull_indices = convex_hull_4d(points_4d)
print(convex_hull_indices)