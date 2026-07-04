





def normalize_shape(shape):
    
    min_x = min(x for x, y in shape)
    min_y = min(y for x, y in shape)
    
    normalized = sorted((x - min_x, y - min_y) for x, y in shape)
    return tuple(normalized)

def get_all_symmetries(shape):
    
    symmetries = []
    current_shape = shape
    
    for _ in range(4):
        
        current_shape = [(y, -x) for x, y in current_shape]
        symmetries.append(normalize_shape(current_shape))
        
        flipped = [(-x, y) for x, y in current_shape]
        symmetries.append(normalize_shape(flipped))
        
    return symmetries

def get_canonical_form(shape):
    
    return min(get_all_symmetries(shape))

def find_polyominoes(max_size):
    
    
    
    results = {i: set() for i in range(1, max_size + 1)}
    
    
    initial_shape = normalize_shape([(0, 0)])
    results[1].add(initial_shape)
    
    
    for size in range(1, max_size):
        for shape in results[size]:
            
            for x, y in shape:
                
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_square = (x + dx, y + dy)
                    if new_square not in shape:
                        
                        new_shape = list(shape) + [new_square]
                        
                        canonical = get_canonical_form(new_shape)
                        results[size + 1].add(canonical)
    return results




max_squares = 5
all_shapes = find_polyominoes(max_squares)


print(f"{'Number of Squares':<20} | {'Unique Shapes (Pieces)':<25}")
print("-" * 50)

for size in range(1, max_squares + 1):
    count = len(all_shapes[size])
    
    print(f"{size:<20} | {count:<25}")


print("\nCalculation complete.")
print("In Blokus Duo, the set of pieces consists of these 21 unique shapes")
print("(1 + 1 + 2 + 5 + 12 = 21 total pieces).")