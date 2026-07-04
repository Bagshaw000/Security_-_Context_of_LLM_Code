import numpy as np
from scipy.spatial import ConvexHull

def convex_hull_4d(points):
    hull = ConvexHull(points)
    return hull.simplices


points_4d = np.random.rand(20, 4)
convex_hull = convex_hull_4d(points_4d)
print(convex_hull)