def generate_shapes(n):
    if n == 1:
        return [((0, 0),)]
    
    shapes = set()
    
    def add_shape(shape):
        
        min_x = min(x for x, y in shape)
        min_y = min(y for x, y in shape)
        normalized = tuple(sorted((x - min_x, y - min_y) for x, y in shape))
        shapes.add(normalized)

    def build_shape(shape, remaining):
        if remaining == 0:
            add_shape(shape)
            return
        
        for x, y in shape:
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                new_square = (x + dx, y + dy)
                if new_square not in shape:
                    build_shape(shape + [new_square], remaining - 1)

    build_shape([(0, 0)], n - 1)
    
    return [shape for shape in shapes]

def count_unique_shapes(max_n):
    all_shapes = {}
    for n in range(1, max_n + 1):
        all_shapes[n] = generate_shapes(n)
    return all_shapes

result = count_unique_shapes(5)
for n, shapes in result.items():
    print(f"{n}-square pieces: {len(shapes)}")