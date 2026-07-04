



def normalize_shape(shape):
    
    min_x = min(square[0] for square in shape)
    min_y = min(square[1] for square in shape)
    
    return tuple(sorted((square[0] - min_x, square[1] - min_y) for square in shape))

def get_all_rotations_and_flips(shape):
    
    variants = []
    current_shape = list(shape)
    
    for _ in range(4):
        
        current_shape = [(s[1], -s[0]) for s in current_shape]
        variants.append(normalize_shape(current_shape))
        
        
        flipped_shape = [(-s[0], s[1]) for s in current_shape]
        variants.append(normalize_shape(flipped_shape))
        
    return variants



current_pieces = {((0, 0),)}
total_blokus_pieces = 0

print("Blokus Duo Piece Calculation")
print("----------------------------")


for size in range(1, 6):
    number_of_unique_pieces = len(current_pieces)
    print(f"Pieces made of {size} square(s): {number_of_unique_pieces}")
    total_blokus_pieces += number_of_unique_pieces
    
    
    if size < 5:
        next_size_pieces = set()
        
        for shape in current_pieces:
            
            
            for x, y in shape:
                
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (x + dx, y + dy)
                    
                    if neighbor not in shape:
                        
                        new_shape = shape + (neighbor,)
                        
                        
                        
                        all_variants = get_all_rotations_and_flips(new_shape)
                        standard_version = min(all_variants)
                        
                        
                        next_size_pieces.add(standard_version)
        
        current_pieces = next_size_pieces

print("----------------------------")
print(f"Total unique pieces in a Blokus Duo set: {total_blokus_pieces}")