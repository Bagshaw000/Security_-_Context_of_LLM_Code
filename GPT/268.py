import numpy as np
from scipy.spatial import ConvexHull

def convex_hull_4d(points):
    
    points = np.array(points)
    
    
    if len(points) < 5:
        raise ValueError("At least 5 points are required to form a convex hull in 4D.")
    
    
    hull = ConvexHull(points)
    
    
    return points[hull.vertices]


points_4d = np.random.rand(10, 4)  
hull_vertices = convex_hull_4d(points_4d)
print(hull_vertices)