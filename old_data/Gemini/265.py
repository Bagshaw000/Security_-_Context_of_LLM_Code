








import numpy as np
from scipy.spatial import ConvexHull






my_points = [
    [0, 0, 0, 0],
    [10, 0, 0, 0],
    [0, 10, 0, 0],
    [0, 0, 10, 0],
    [0, 0, 0, 10],
    [2, 2, 2, 2],  
    [1, 1, 1, 1],  
    [5, 5, 5, 5]   
]


points_array = np.array(my_points)


try:
    
    hull = ConvexHull(points_array)

    
    print("CONVEX HULL COMPLETED")
    print("---------------------")

    
    print("These are the row numbers of the points that form the outer shell:")
    print(hull.vertices)

    print("\nThese are the actual 4D coordinates of those 'outer' points:")
    for index in hull.vertices:
        print(my_points[index])

    
    print("\nThese are the connections between points that form the surface faces:")
    print(hull.simplices)

    print("\nTotal volume of this 4D shape:")
    print(hull.volume)

except Exception as e:
    print("Something went wrong.")
    print("Note: For 4D calculations, you need at least 5 points.")
    print("Also, the points cannot all be in a perfectly flat line.")
    print("Error details:", e)

