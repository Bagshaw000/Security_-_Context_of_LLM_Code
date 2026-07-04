







import numpy as np
from scipy.spatial import ConvexHull

def find_the_outer_shell():
    
    
    
    
    points_list = [
        [1, 1, 1, 1],
        [10, 1, 1, 1],
        [1, 10, 1, 1],
        [1, 1, 10, 1],
        [1, 1, 1, 10],
        [2, 2, 2, 2],  
        [3, 3, 3, 3],  
        [4, 4, 4, 4]   
    ]

    
    data_points = np.array(points_list)

    try:
        
        
        
        hull = ConvexHull(data_points)

        print("--- ANALYSIS COMPLETE ---")
        
        
        
        print("The row numbers that form the outer boundary are:")
        print(hull.vertices)

        
        
        print("\nThe groups of points that form the outer surfaces (walls):")
        for surface in hull.simplices:
            print(surface)

    except Exception as error:
        print("The computer couldn't calculate the shell.")
        print("This usually happens if the points are too close together or flat.")
        print(f"Error details: {error}")


find_the_outer_shell()