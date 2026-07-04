







import numpy as np
from scipy.spatial import ConvexHull





points_list = [
    [0, 0, 0, 0],
    [5, 0, 0, 0],
    [0, 5, 0, 0],
    [0, 0, 5, 0],
    [0, 0, 0, 5],
    [1, 1, 1, 1], 
    [2, 1, 0, 1], 
    [5, 5, 5, 5]  
]


points = np.array(points_list)

def calculate_4d_shell(data_points):
    try:
        
        
        hull = ConvexHull(data_points)

        print("--- HAROLD'S 4D CONVEX HULL RESULTS ---")
        
        
        
        print(f"The points at these row indices form the outer boundary:")
        print(hull.vertices)

        print("\nIn 4D geometry, the 'faces' of the shape are 3D volumes.")
        print(f"This shape has {len(hull.simplices)} distinct outer surfaces:")
        
        for i, surface in enumerate(hull.simplices):
            
            print(f"  Surface {i + 1} is made by connecting point indices: {surface}")

        
        print(f"\nTotal 4D Hypervolume: {hull.volume:.2f}")
        
        
        print(f"Total 3D Surface Area: {hull.area:.2f}")

    except Exception as e:
        
        
        print("Error: Could not calculate the shell.")
        print(f"This usually means the points don't spread out into 4 dimensions: {e}")


if __name__ == "__main__":
    calculate_4d_shell(points)




