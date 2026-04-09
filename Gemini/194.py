def get_canonical_form(points):
    
    
    symmetries = []
    current = points
    for _ in range(4):
        
        current = [(p[1], -p[0]) for p in current]
        
        for shape in [current, [(p[0], -p[1]) for p in current]]:
            
            min_x = min(pt[0] for pt in shape)
            min_y = min(pt[1] for pt in shape)
            normalized = tuple(sorted((pt[0] - min_x, pt[1] - min_y) for pt in shape))
            symmetries.append(normalized)
    
    return min(symmetries)

def run_blokus_calculation():
    
    pieces_by_size = {1: {((0, 0),)}}
    
    
    for size in range(1, 5):
        next_gen = set()
        for piece in pieces_by_size[size]:
            for x, y in piece:
                
                for dx, dy in [(1,