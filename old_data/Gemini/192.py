





def get_canonical(shape):
    
    variants = []
    curr = list(shape)
    
    
    for _ in range(4):
        
        curr = [(p[1], -p[0]) for p in curr]
        
        for flip in [False, True]:
            if flip:
                temp = [(-p[0], p[1]) for p in curr]
            else:
                temp = list(curr)
            
            
            
            min_x = min(p[0] for p in temp)
            min_y = min(p[1] for p in temp)
            normalized = tuple(sorted((p[0] - min_x, p[1] - min_y) for p in temp))
            variants.append(normalized)
    
    
    return min(variants)

def find_pieces(max_size):
    
    
    pieces_by_size = {1: {((0, 0),)}}
    
    for n in range(1, max_size):
        next_size = n + 1
        new_shapes = set()
        
        
        
        for shape in pieces_by_size[n]:
            for x, y in shape:
                
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_sq = (x + dx, y + dy)
                    if new_sq not in shape:
                        
                        new_shape = shape + (new_sq,)
                        
                        new_shapes.add(get_canonical(new_shape))
        
        pieces_by_size[next_size] = new_shapes
        
    return pieces_by_size


results = find_pieces(5)


total_pieces = 0
print("Blokus Duo Piece Count Analysis")
print("===============================")
for size, shapes in results.items():
    count = len(shapes)
    total_pieces += count
    print(f"Pieces made of {size} square(s): {count}")

print("===============================")
print(f"Total unique pieces in the game: {total_pieces}")







