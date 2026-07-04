














def get_canonical_form(shape):
    
    def rotate(coords):
        return [(y, -x) for x, y in coords]

    def flip(coords):
        return [(x, -y) for x, y in coords]

    def normalize(coords):
        
        min_x = min(p[0] for p in coords)
        min_y = min(p[1] for p in coords)
        return sorted((x - min_x, y - min_y) for x, y in coords)

    symmetries = []
    current = list(shape)
    
    
    for _ in range(4):
        current = rotate(current)
        symmetries.append(normalize(current))
        symmetries.append(normalize(flip(current)))

    
    return tuple(min(symmetries))

def generate_blokus_pieces(max_size):
    
    
    
    all_pieces = {1: {((0, 0),)}}

    for size in range(1, max_size):
        if size not in all_pieces:
            continue
            
        next_size = size + 1
        all_pieces[next_size] = set()

        for shape in all_pieces[size]:
            
            for x, y in shape:
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_square = (x + dx, y + dy)
                    
                    if new_square not in shape:
                        
                        new_shape = list(shape) + [new_square]
                        
                        canonical = get_canonical_form(new_shape)
                        all_pieces[next_size].add(canonical)
                        
    return all_pieces

def display_pieces():
    
    
    MAX_SQUARE_SIZE = 5
    
    
    try:
        limit = int(MAX_SQUARE_SIZE)
    except ValueError:
        print("Error: Invalid size provided.")
        return

    print("--- BLOKUS DUO PIECE GENERATOR ---")
    results = generate_blokus_pieces(limit)
    
    total_count = 0
    for size in range(1, limit + 1):
        pieces = results[size]
        count = len(pieces)
        total_count += count
        print(f"Size {size}: {count} unique pieces found.")
        
        
        
        for i, piece in enumerate(sorted(pieces), 1):
            print(f"  Piece {i}: {piece}")
            
    print("-" * 34)
    print(f"Total unique pieces (1-5 squares): {total_count}")
    print("Generation complete and secure.")


if __name__ == "__main__":
    display_pieces()






