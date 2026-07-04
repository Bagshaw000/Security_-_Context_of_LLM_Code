def generate_shapes(n):
    if n == 1:
        return [((0, 0),)]
    elif n == 2:
        return [((0, 0), (1, 0))]
    elif n == 3:
        return [((0, 0), (1, 0), (2, 0)), ((0, 0), (1, 0), (1, 1))]
    elif n == 4:
        return [((0, 0), (1, 0), (2, 0), (3, 0)), 
                ((0, 0), (1, 0), (1, 1), (1, 2)), 
                ((0, 0), (1, 0), (0, 1), (1, 1))]
    elif n == 5:
        return [((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)), 
                ((0, 0), (1, 0), (1, 1), (1, 2), (2, 2)), 
                ((0, 0), (1, 0), (0, 1), (1, 1), (1, 2))]
    return []

def rotate(shape):
    return [(y, -x) for x, y in shape]

def flip(shape):
    return [(-x, y) for x, y in shape]

def unique_shapes(n):
    shapes = generate_shapes(n)
    unique = set()
    
    for shape in shapes:
        transformations = set()
        current = shape
        
        for _ in range(4):
            current = rotate(current)
            transformations.add(tuple(sorted(current)))
            transformations.add(tuple(sorted(flip(current))))
        
        unique.update(transformations)
    
    return len(unique)

total_shapes = sum(unique_shapes(n) for n in range(1, 6))
print(total_shapes)