def generate_shapes(n):
    from itertools import product

    def rotate(shape):
        return set((y, -x) for x, y in shape)

    def flip(shape):
        return set((-x, y) for x, y in shape)

    def normalize(shape):
        return frozenset((x - min_x, y - min_y) for x, y in shape)

    def all_variants(shape):
        variants = set()
        current = shape
        for _ in range(4):
            current = rotate(current)
            variants.add(normalize(current))
            variants.add(normalize(flip(current)))
        return variants

    def add_shapes(shape1, shape2):
        return set((x + dx, y + dy) for x, y in shape1 for dx, dy in shape2)

    def can_place(shape, occupied):
        return all((x, y) not in occupied for x, y in shape)

    def place_shape(shape, occupied):
        return occupied.union(shape)

    def find_shapes(n, occupied=set()):
        if n == 0:
            return {frozenset()}
        shapes = set()
        for shape in find_shapes(n - 1, occupied):
            for dx, dy in product(range(-1, 2), repeat=2):
                new_shape = add_shapes(shape, {(dx, dy)})
                if can_place(new_shape, occupied):
                    shapes.update(all_variants(new_shape))
        return shapes

    return find_shapes(n)

def count_unique_shapes(max_n):
    unique_shapes = set()
    for n in range(1, max_n + 1):
        shapes = generate_shapes(n)
        unique_shapes.update(shapes)
    return len(unique_shapes)

print(count_unique_shapes(5))