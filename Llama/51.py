from typing import List
import numpy as np

def orientation(p: tuple, q: tuple, r: tuple) -> int:
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2

def convex_hull(points: List[tuple]) -> List[tuple]:
    n = len(points)
    hull = []
    leftmost = min(range(n), key=lambda i: points[i])
    p = leftmost
    while True:
        hull.append(points[p])
        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
        p = q
        if p == leftmost:
            break
    return hull


points = [(0, 3), (1, 1), (2, 2), (4, 4)]
hull_points = convex_hull(points)
print(hull_points)