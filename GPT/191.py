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
    return tuple((y, -x) for x, y in shape)

def flip(shape):
    return tuple((-x, y) for x, y in shape)

def unique_shapes(n):
    shapes = generate_shapes(n)
    unique = set()
    
    for shape in shapes:
        transformations = set()
        current = shape
        
        for _ in range(4):
            current = rotate(current)
            transformations.add(current)
            transformations.add(flip(current))
        
        unique.add(min(transformations))
    
    return unique

def count_unique_shapes(max_n):
    total = 0
    for n in range(1, max_n + 1):
        unique = unique_shapes(n)
        total += len(unique)
    return total

result = count_unique_shapes(5)
print(result)