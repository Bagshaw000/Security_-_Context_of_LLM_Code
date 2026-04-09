import numpy as np
from scipy.spatial import ConvexHull

def convex_hull_4d(points):
    hull = ConvexHull(points)
    return hull.vertices