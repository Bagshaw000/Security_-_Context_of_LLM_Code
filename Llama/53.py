import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2 + (p1[3] - p2[3])**2)

def compare(p1, p2):
    if p1 == p2:
        return 0
    elif distance(p1, p2) > 0.00001:
        return 1
    else:
        return -1

def convex_hull(points):
    n = len(points)
    hull = []
    for i in range(n):
        if not (i < n-1 and points[i][2] == points[i+1][2] and points[i][3] == points[i+1][3]):
            l = 0
            while l != i:
                if compare(points[l], points[(l + 1) % n]) > 0:
                    break
                l += 1
            r = (i + 1) % n
            while r != i:
                if compare(points[r], points[(r - 1) % n]) > 0:
                    break
                r -= 1
            hull.append(points[i])
            while l != i and compare(points[l], points[(l + 1) % n]) < 0:
                hull[-1] = points[(l+1)%n]
                l += 1
    return hull

points = [(0,0,0,0), (3,4,5,6), (2,7,8,9)]
print(convex_hull(points))