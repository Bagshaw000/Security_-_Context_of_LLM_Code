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
        for _ in range(4):  
            shape = rotate(shape)
            unique.add(tuple(sorted(shape)))
            unique.add(tuple(sorted(flip(shape))))
    
    return unique

def count_unique_shapes(max_n):
    total_shapes = {}
    for n in range(1, max_n + 1):
        total_shapes[n] = len(unique_shapes(n))
    return total_shapes

result = count_unique_shapes(5)
print(result)