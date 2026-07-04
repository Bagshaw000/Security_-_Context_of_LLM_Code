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
                ((0, 0), (1, 0), (0, 1), (0, 2))]
    elif n == 5:
        return [((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)), 
                ((0, 0), (1, 0), (1, 1), (1, 2), (1, 3)), 
                ((0, 0), (1, 0), (0, 1), (0, 2), (1, 2))]
    return []

def rotate(shape):
    return tuple((y, -x) for x, y in shape)

def flip(shape):
    return tuple((-x, y) for x, y in shape)

def normalize(shape):
    return tuple(sorted((x - min_x, y - min_y) for x, y in shape))
    
def unique_shapes(n):
    shapes = generate_shapes(n)
    unique = set()
    
    for shape in shapes:
        for _ in range(4):
            shape = rotate(shape)
            unique.add(normalize(shape))
            unique.add(normalize(flip(shape)))
    
    return len(unique)

total_shapes = sum(unique_shapes(n) for n in range(1, 6))
print(total_shapes)