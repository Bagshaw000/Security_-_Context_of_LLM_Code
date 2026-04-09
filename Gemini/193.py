



def get_standard_orientation(piece):
    
    all_orientations = []
    current_squares = list(piece)
    
    
    for flip in range(2):
        for rotation in range(4):
            
            current_squares = [(y, -x) for x, y in current_squares]
            
            
            min_x = min(x for x, y in current_squares)
            min_y = min(y for x, y in current_squares)
            standardized = sorted([(x - min_x, y - min_y) for x, y in current_squares])
            
            
            all_orientations.append(tuple(standardized))
        
        
        current_squares = [(x, -y) for x, y in current_squares]
        
    
    return min(all_orientations)

def find_all_blokus_pieces():
    
    
    pieces_by_size = {}
    
    
    pieces_by_size[1] = {((0, 0),)}
    
    
    for current_size in range(2, 6):
        new_shapes = set()
        
        for existing_piece in pieces_by_size[current_size - 1]:
            
            for x, y in existing_piece:
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in existing_piece:
                        
                        new_piece = list(existing_piece) + [neighbor]
                        
                        standard_version = get_standard_orientation(new_piece)
                        new_shapes.add(standard_version)
        
        pieces_by_size[current_size] = new_shapes
        
    return pieces_by_size




all_results = find_all_blokus_pieces()

print("BLOKUS DUO: PIECE VARIATIONS REPORT")
print("------------------------------------")

total_count = 0
for size in range(1, 6):
    number_of_variations = len(all_results[size])
    total_count += number_of_variations
    print("Pieces made of " + str(size) + " square(s): " + str(number_of_variations))

print("------------------------------------")
print("Total unique pieces in the game: " + str(total_count))
