from itertools import product

def rotate(shape):
    return set((y, -x) for x, y in shape)

def reflect(shape):
    return set((-x, y) for x, y in shape)

def generate_shapes(n):
    if n == 1:
        return [{(0, 0)}]
    
    shapes = set()
    for smaller_shape in generate_shapes(n - 1):
        for x, y in smaller_shape:
            new_shape = smaller_shape | {(x + 1, y), (x, y + 1)}
            shapes.add(frozenset(new_shape))
            shapes.add(frozenset(rotate(new_shape)))
            shapes.add(frozenset(reflect(new_shape)))
    
    return shapes

def unique_shapes(n):
    shapes = generate_shapes(n)
    unique = set()
    for shape in shapes:
        unique.add(frozenset(shape))
    return len(unique)

def blokus_shapes():
    total_shapes = {}
    for n in range(1, 6):
        total_shapes[n] = unique_shapes(n)
    return total_shapes

print(blokus_shapes())