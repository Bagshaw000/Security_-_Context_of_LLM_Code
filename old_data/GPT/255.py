import numpy as np
from scipy.spatial import ConvexHull

def convex_hull_4d(points):
    
    points = np.array(points)
    
    
    hull = ConvexHull(points)
    
    
    return points[hull.vertices]


points_4d = np.random.rand(10, 4)  
hull_vertices = convex_hull_4d(points_4d)
print(hull_vertices)