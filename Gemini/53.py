





import numpy as np
from scipy.spatial import ConvexHull
import sys









my_points = [
    [0, 0, 0, 0],
    [10, 0, 0, 0],
    [0, 10, 0, 0],
    [0, 0, 10, 0],
    [0, 0, 0, 10],
    [2, 2, 2, 2],  
    [5, 1, 1, 1],  
    [1, 5, 1, 1],
    [1, 1, 5, 1],
    [1, 1, 1, 5]
]

def run_convex_hull_algorithm(data_list):
    
    points_array = np.array(data_list)
    
    
    
    if len(points_array) < 5:
        print("Error: You need at least 5 points to calculate a 4D hull.")
        return

    try:
        
        
        
        
        
        hull = ConvexHull(points_array)

        
        
        
        print("--- CONVEX HULL RESULTS ---")
        print(f"Total points provided: {len(data_list)}")
        print(f"Points that actually form the outer shell: {len(hull.vertices)}")
        print("")

        
        
        print("The following sets of points form the outer boundary faces:")
        print("(The numbers represent the row index from your data, starting at 0)")
        
        for i, face in enumerate(hull.simplices):
            
            print(f"Face {i+1}: Points {face}")

        print("\n--- MEASUREMENTS ---")
        
        print(f"Surface Area (3D boundary volume): {hull.area:.2f}")
        
        print(f"Hyper-volume (4D space enclosed): {hull.volume:.2f}")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("This usually happens if the points are too flat or all on the same line.")


if __name__ == "__main__":
    run_convex_hull_algorithm(my_points)





