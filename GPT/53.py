def convex_hull_4d(points):
    from scipy.spatial import ConvexHull
    import numpy as np

    points = np.array(points)
    hull = ConvexHull(points)

    return [points[vertex] for vertex in hull.vertices]


points_4d = [
    [1, 2, 3, 4],
    [2, 3, 4, 5],
    [3, 4, 5, 6],
    [1, 1, 1, 1],
    [0, 0, 0, 0]
]

hull_points = convex_hull_4d(points_4d)
print(hull_points)