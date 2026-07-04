



def get_all_orientations(shape):
    
    orientations = []
    current = list(shape)
    for _ in range(4):
        
        current = [(y, -x) for x, y in current]
        orientations.append(set(current))
        
        
        reflected = [(-x, y) for x, y in current]
        orientations.append(set(reflected))
    return orientations

def move_to_origin(shape):
    
    min_x = min(x for x, y in shape)
    min_y = min(y for x, y in shape)
    
    return tuple(sorted((x - min_x, y - min_y) for x, y in shape))

def calculate_blokus_pieces(max_squares):
    
    
    current_shapes = {((0, 0),)}
    results = {}

    for size in range(1, max_squares + 1):
        
        results[size] = len(current_shapes)
        
        
        if size == max_squares:
            break
        
        next_generation = set()
        for shape in current_shapes:
            
            for x, y in shape:
                
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in shape:
                        
                        new_shape = set(shape)
                        new_shape.add(neighbor)
                        
                        
                        variants = get_all_orientations(new_shape)
                        
                        
                        
                        standard_version = min(move_to_origin(v) for v in variants)
                        next_generation.add(standard_version)
        
        current_shapes = next_generation
        
    return results


max_size = 5
piece_data = calculate_blokus_pieces(max_size)


print("BLOKUS DUO PIECE ANALYSIS")
print("-------------------------")
total_pieces = 0
for size, count in piece_data.items():
    print(f"Shapes made of {size} square(s): {count}")
    total_pieces += count

print("-------------------------")
print(f"Total unique pieces in the game: {total_pieces}")