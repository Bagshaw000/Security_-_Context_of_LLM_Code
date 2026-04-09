import numpy as np

def convex_hull_4d(points):
    
    from scipy.spatial import ConvexHull
    
    
    points = np.array(points)
    
    
    hull = ConvexHull(points)
    
    
    return points[hull.vertices]