



import numpy as np
from scipy.spatial import ConvexHull





my_points = [
    [0, 0, 0, 0],
    [10, 0, 0, 0],
    [0, 10, 0, 0],
    [0, 0, 10, 0],
    [0, 0, 0, 10],
    [2, 2, 2, 2],  
    [1, 1, 1, 1]   
]


points_array = np.array(my_points)

try:
    
    
    hull = ConvexHull(points_array)

    print("Success! The outer shell has been calculated.")
    print("-" * 40)

    
    
    print("The points that form the boundary faces are:")
    for face in hull.simplices:
        print(f"Face composed of point indices: {face}")

    print("-" * 40)
    
    print(f"Total 4D Volume: {hull.volume:.2f}")
    
    
    print(f"Total Surface Area: {hull.area:.2f}")

except Exception as e:
    print("The calculation could not be completed.")
    print("Note: To form a 4D shape, you need at least 5 points that are not all on the same flat plane.")
    print(f"Error details: {e}")




