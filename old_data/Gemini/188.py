import collections

def get_canonical_representation(polyomino):
    
    def normalize(coords):
        min_x = min(c[0] for c in coords)
        min_y = min(c[1] for c in coords)
        return tuple(sorted((c[0] - min_x, c[1] - min_y) for c in coords))

    symmetries = []
    current_coords = list(polyomino)
    
    for _ in range(4):
        
        current_coords = [(c[1], -c[0]) for c in current_coords]
        symmetries.append(normalize(current_coords))
        
        
        reflected = [(-c[0], c[1]) for c in current_coords]
        symmetries.append(normalize(reflected))
        
    return min(symmetries)

def generate_free_polyominoes(max_n):
    
    
    pieces_by_size = collections.defaultdict(set)
    
    
    monomino = ((0, 0),)
    pieces_by_size[1].add(monomino)
    
    for n in range(1, max_n):
        for piece in pieces_by_size[n]:
            
            for x, y in piece:
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in piece:
                        
                        new_piece = piece + (neighbor,)
                        
                        canonical = get_canonical_representation(new_piece)
                        pieces_by_size[n + 1].add(canonical)
                        
    return pieces_by_size

def run_blokus_analysis():
    
    max_n = 5
    results = generate_free_polyominoes(max_n)
    
    print(f"Blokus Duo Piece Analysis (n=1 to {max_n})")
    print("=" * 40)
    
    total_pieces = 0
    total_squares = 0
    
    for n in sorted(results.keys()):
        count = len(results[n])
        total_pieces += count
        total_squares += (count * n)
        print(f"n = {n}: {count:>2} unique pieces")
        
    print("=" * 40)
    print(f"Total Unique Pieces per Player: {total_pieces}")
    print(f"Total Squares per Player:       {total_squares}")

if __name__ == "__main__":
    run_blokus_analysis()