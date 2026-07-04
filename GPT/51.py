from scipy.spatial import ConvexHull
import numpy as np

def convex_hull_4d(points):
    if len(points) < 5:
        raise ValueError("At least 5 points are required to form a convex hull in 4D.")
    
    points = np.array(points)
    hull = ConvexHull(points)
    
    return hull.vertices


points_4d = [
    [1, 2, 3, 4],
    [2, 3, 4, 5],
    [3, 4, 5, 6],
    [4, 5, 6, 7],
    [5, 6, 7, 8],
    [1, 1, 1, 1],
    [0, 0, 0, 0]
]

hull_vertices = convex_hull_4d(points_4d)
print("Convex Hull Vertices:", hull_vertices)