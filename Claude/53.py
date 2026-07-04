import numpy as np

def convex_hull(points):
    
    
    points_h = np.hstack((points, np.ones((points.shape[0], 1))))
    
    
    hull = []
    for i in range(points.shape[0]):
        
        c = -points_h[i]
        A_ub = np.delete(points_h, i, 0)
        b_ub = np.zeros(A_ub.shape[0])
        res = scipy.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub)
        
        
        if np.abs(res.fun - 1) < 1e-6:
            hull.append(points[i])
    
    return np.array(hull)