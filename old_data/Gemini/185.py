def get_canonical(poly):
    
    def rotate(p):
        return [(y, -x) for x, y in p]

    def reflect(p):
        return [(x, -y) for x, y in p]

    def normalize(p):
        min_x = min(x for x, y in p)
        min_y = min(y for x, y in p)
        return tuple(sorted((x - min_x, y - min_y) for x, y in p))

    symmetries = []
    current = list(poly)
    for _ in range(4):
        symmetries.append(normalize(current))
        symmetries.append(normalize(reflect(current)))
        current = rotate(current)
    
    
    return min(symmetries)

def generate_blokus_duo_pieces(max_n=5):
    
    
    poly_sets = {1: {((0, 0),)}}
    
    for n in range(2, max_n + 1):
        new_shapes = set()
        
        for poly in poly_sets[n-1]:
            
            for x, y in poly:
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in poly:
                        candidate = list(poly) + [(nx, ny)]
                        new_shapes.add(get_canonical(candidate))
        poly_sets[n] = new_shapes
        
    return poly_sets

def main():
    
    max_size = 5
    piece_data = generate_blokus_duo_pieces(max_size)
    
    total_pieces = 0
    print(f"{'Piece Size (n)':<15} | {'Unique Shapes':<15}")
    print("-" * 35)
    
    for n in range(1, max_size + 1):
        count = len(piece_data[n])
        print(f"{n + 0:<15} | {count:<15}")
        total_pieces += count
        
    print("-" * 35)
    print(f"Total Unique Pieces: {total_pieces}")
    print("\nPiece Breakdown:")
    print("- 1 Monomino (1x1)")
    print("- 1 Domino   (1x2)")
    print("- 2 Trominoes")
    print("- 5 Tetrominoes")
    print("- 12 Pentominoes")

if __name__ == "__main__":
    main()