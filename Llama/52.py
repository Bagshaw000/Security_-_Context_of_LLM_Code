import numpy as np

def convex_hull_4d(points):
    n = len(points)
    hull = []
    for i in range(n):
        if len(hull) == 0 or points[hull[-1]][2] < points[i][2]:
            hull.append(i)

    def cross(p, q, r):
        return (q[1] - p[1]) * (r[2] - p[2]) - (q[0] - p[0]) * (r[1] - p[1])

    def orient(p, q, r):
        val = cross(p, q, r)
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    for i in range(len(hull)):
        p = hull[i]
        q = (hull[(i + 1) % len(hull)] + points[p][3:])
        r = (hull[(i - 1 + len(hull)) % len(hull)] + points[p][3:])
        if orient(q, r, points[p]) == 2:
            hull.remove(p)
    return np.array(hull)

points = [(0, 0, 0, 1), (1, 1, 1, 2), (2, 2, 2, 3), (3, 3, 3, 4), (4, 4, 4, 5)]
print(convex_hull_4d(points))