def rotate(shape):
    return [(y, -x) for x, y in shape]

def flip(shape):
    return [(-x, y) for x, y in shape]

def normalize(shape):
    min_x = min(x for x, y in shape)
    min_y = min(y for x, y in shape)
    return sorted((x - min_x, y - min_y) for x, y in shape)

def generate_shapes(n):
    if n == 1:
        return [{(0, 0)}]
    
    shapes = set()
    for smaller_shape in generate_shapes(n - 1):
        for x, y in smaller_shape:
            new_shape = smaller_shape | {(x + 1, y), (x, y + 1)}
            shapes.add(frozenset(normalize(new_shape)))
            new_shape = smaller_shape | {(x + 1, y), (x, y - 1)}
            shapes.add(frozenset(normalize(new_shape)))
            new_shape = smaller_shape | {(x - 1, y), (x, y + 1)}
            shapes.add(frozenset(normalize(new_shape)))
            new_shape = smaller_shape | {(x - 1, y), (x, y - 1)}
            shapes.add(frozenset(normalize(new_shape)))
    
    return [frozenset(shape) for shape in shapes]

def unique_shapes(n):
    all_shapes = generate_shapes(n)
    unique_shapes = set()
    
    for shape in all_shapes:
        rotations = {normalize(rotate(shape))}
        flipped = flip(shape)
        rotations.add(normalize(flipped))
        
        for _ in range(3):
            flipped = rotate(flipped)
            rotations.add(normalize(flipped))
        
        unique_shapes.add(min(rotations))
    
    return len(unique_shapes)

for i in range(1, 6):
    print(f"Unique {i}-square pieces: {unique_shapes(i)}")