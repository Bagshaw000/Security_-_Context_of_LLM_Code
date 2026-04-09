


def calculate_blokus_pieces():
    
    
    
    def get_standard_form(shape):
        
        
        min_x = min(square[0] for square in shape)
        min_y = min(square[1] for square in shape)
        return tuple(sorted((square[0] - min_x, square[1] - min_y) for square in shape))

    def get_all_possible_views(shape):
        
        
        views = set()
        current = shape
        for _ in range(4):
            
            current = get_standard_form([(square[1], -square[0]) for square in current])
            views.add(current)
            
            flipped = get_standard_form([(-square[0], square[1]) for square in current])
            views.add(flipped)
        return views

    
    
    pieces_by_size = {1: {((0, 0),)}}
    
    
    for size in range(1, 5):
        next_size = size + 1
        found_shapes = set()
        
        for existing_shape in pieces_by_size[size]:
            
            for x, y in existing_shape:
                
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    neighbor = (x + dx, y + dy)
                    
                    
                    if neighbor not in existing_shape:
                        candidate = get_standard_form(list(existing_shape) + [neighbor])
                        
                        
                        if not any(view in found_shapes for view in get_all_possible_views(candidate)):
                            found_shapes.add(candidate)
        
        pieces_by_size[next_size] = found_shapes
    
    return pieces_by_size


results = calculate_blokus_pieces()
grand_total = 0

print("BLOKUS DUO PIECE ANALYSIS")
print("==========================")

for n in range(1, 6):
    count = len(results[n])
    grand_total += count
    print("Unique pieces made of " + str(n) + " square(s): " + str(count))

print("==========================")
print("Total unique pieces in a set: " + str(grand_total))
print("This matches the 21 pieces found in a standard Blokus Duo game.")