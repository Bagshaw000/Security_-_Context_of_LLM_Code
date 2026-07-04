

















def is_point_outside_line(p1, p2, test_point):
    
    
    try:
        value = (p2[0] - p1[0]) * (test_point[1] - p1[1]) - (p2[1] - p1[1]) * (test_point[0] - p1[0])
        return value > 0
    except:
        return False

def find_convex_hull_2d(points):
    
    
    
    if len(points) < 3:
        return points
    
    
    leftmost = min(points, key=lambda p: (p[0], p[1]))
    
    hull = []
    current = leftmost
    
    
    while True:
        hull.append(current)
        next_point = points[0]
        
        
        for point in points:
            if point == current:
                continue
            
            
            if next_point == current or is_point_outside_line(current, next_point, point):
                next_point = point
        
        current = next_point
        
        
        if current == leftmost:
            break
    
    return hull

def explain_four_dimensions():
    
    
    print("=" * 50)
    print("UNDERSTANDING CONVEX HULLS - SIMPLE EXPLANATION")
    print("=" * 50)
    print()
    
    print("2D EXAMPLE (points on a flat piece of paper):")
    print("-" * 50)
    
    
    points_2d = [
        (0, 0),
        (1, 1),
        (2, 0),
        (1, 2),
        (0.5, 0.5)
    ]
    
    print("Our points are:")
    for i, point in enumerate(points_2d):
        print(f"  Point {i+1}: {point}")
    
    print()
    print("The convex hull (outer boundary) includes:")
    
    try:
        hull = find_convex_hull_2d(points_2d)
        for i, point in enumerate(hull):
            print(f"  Point {i+1}: {point}")
    except Exception as error:
        print(f"  Error calculating hull: {error}")
    
    print()
    print("=" * 50)
    print("4D EXAMPLE (harder to imagine):")
    print("-" * 50)
    print()
    print("Instead of X and Y coordinates, imagine we have 4 measurements:")
    print("  - Coordinate 1 (like X)")
    print("  - Coordinate 2 (like Y)")
    print("  - Coordinate 3 (like Z, for height)")
    print("  - Coordinate 4 (something extra, like time)")
    print()
    
    points_4d = [
        (0, 0, 0, 0),
        (1, 1, 1, 1),
        (2, 0, 1, 0),
        (0, 2, 1, 1),
        (1, 1, 0.5, 0.5)
    ]
    
    print("Our 4D points are:")
    for i, point in enumerate(points_4d):
        print(f"  Point {i+1}: {point}")
    
    print()
    print("NOTE: Finding the convex hull in 4D is very complicated!")
    print("It requires special mathematical techniques that are beyond")
    print("simple explanations. But the idea is the same - finding the")
    print("outermost points that form a boundary around all points.")
    print()

def simple_distance_calculator():
    
    
    
    print("=" * 50)
    print("DISTANCE BETWEEN 4D POINTS (simpler operation)")
    print("=" * 50)
    print()
    
    point_a = (0, 0, 0, 0)
    point_b = (1, 1, 1, 1)
    
    print(f"Point A: {point_a}")
    print(f"Point B: {point_b}")
    print()
    
    try:
        
        distance = 0
        
        for i in range(len(point_a)):
            difference = point_b[i] - point_a[i]
            distance = distance + (difference * difference)
        
        
        distance = distance ** 0.5
        
        print(f"Distance between the points: {distance:.2f}")
        
    except Exception as error:
        print(f"Error calculating distance: {error}")
    
    print()

def main():
    
    
    print()
    print("WELCOME TO CONVEX HULL BASICS")
    print("(No special libraries, just basic Python)")
    print()
    
    
    explain_four_dimensions()
    simple_distance_calculator()
    
    print("=" * 50)
    print("KEY TAKEAWAYS:")
    print("=" * 50)
    print()
    print("1. A convex hull is like a rubber band stretched around")
    print("   the outermost points in a set of data.")
    print()
    print("2. In 2D, it's easy to picture - like an outline on paper.")
    print()
    print("3. In 4D, we can't easily visualize it, but the math works")
    print("   the same way - just with 4 numbers per point instead of 2.")
    print()
    print("4. This concept is useful in many real-world applications")
    print("   like computer graphics, data analysis, and optimization.")
    print()

if __name__ == "__main__":
    main()