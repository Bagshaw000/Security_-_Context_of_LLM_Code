







import numpy as np
from scipy.spatial import ConvexHull




points_list = [
    [0, 0, 0, 0],
    [10, 0, 0, 0],
    [0, 10, 0, 0],
    [0, 0, 10, 0],
    [0, 0, 0, 10],
    [2, 2, 2, 2],  
    [1, 1, 1, 1],  
    [5, 5, 5, 5]   
]


points_table = np.array(points_list)






try:
    
    hull = ConvexHull(points_table)

    
    print("CONVEX HULL CALCULATION RESULTS")
    print("===============================")

    
    
    print("The row numbers in your table that form the outer shell are:")
    print(hull.vertices)

    print("\nThe actual coordinates of those outer points are:")
    for row_index in hull.vertices:
        print(points_list[row_index])

    
    
    
    print("\nThe total 4-dimensional volume of this shape is:")
    print(hull.volume)

    
    print("\nThe total 'surface area' (the size of the outer skin) is:")
    print(hull.area)

except Exception as e:
    
    
    print("An error occurred during the calculation:")
    print(e)



