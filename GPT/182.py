def generate_shapes(n):
    if n == 1:
        return [((0, 0),)]
    
    shapes = set()
    
    def add_shape(shape):
        
        min_x = min(x for x, y in shape)
        min_y = min(y for x, y in shape)
        normalized = tuple(sorted((x - min_x, y - min_y) for x, y in shape))
        shapes.add(normalized)

    def dfs(shape, x, y):
        if len(shape) == n:
            add_shape(shape)
            return
        
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) not in shape:
                dfs(shape + [(new_x, new_y)], new_x, new_y)

    dfs([(0, 0)], 0, 0)
    return shapes

def count_unique_shapes(max_n):
    total_shapes = {}
    for n in range(1, max_n + 1):
        shapes = generate_shapes(n)
        total_shapes[n] = len(shapes)
    return total_shapes

result = count_unique_shapes(5)
print(result)