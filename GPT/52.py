import numpy as np
from scipy.spatial import ConvexHull

class ConvexHull4D:
    def __init__(self, points):
        self.points = np.array(points)
        self.hull = None

    def compute_hull(self):
        if self.points.shape[1] != 4:
            raise ValueError("Points must be in 4D space.")
        self.hull = ConvexHull(self.points)

    def get_hull_vertices(self):
        if self.hull is None:
            raise ValueError("Convex hull has not been computed yet.")
        return self.points[self.hull.vertices]


if __name__ == "__main__":
    points_4d = [
        [1, 2, 3, 4],
        [2, 3, 4, 5],
        [3, 4, 5, 6],
        [4, 5, 6, 7],
        [5, 6, 7, 8],
        [1, 3, 2, 4],
        [2, 4, 3, 5],
        [3, 5, 4, 6]
    ]
    
    hull = ConvexHull4D(points_4d)
    hull.compute_hull()
    vertices = hull.get_hull_vertices()
    print("Convex Hull Vertices:\n", vertices)