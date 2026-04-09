import collections

def get_canonical(shape):
    
    def normalize(coords):
        min_x = min(c[0] for c in coords)
        min_y = min(c[1] for c in coords)
        return tuple(sorted((c[0] - min_x, c[1] - min_y) for c in coords))

    candidates = []
    curr = list(shape)
    
    for _ in range(4):
        
        curr = [(y, -x) for x, y in curr]
        candidates.append(normalize(curr))
        
        reflected = [(-x, y) for x, y in curr]
        candidates.append(normalize(reflected))
        
    return min(candidates)

def generate_polyominoes(max_n):
    
    
    poly_sets = {1: {((0, 0),)}}
    
    for n in range(2, max_n + 1):
        next_gen = set()
        for poly in poly_sets[n-1]:
            
            for x, y in poly:
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in poly:
                        
                        new_poly = poly + ((nx, ny),)
                        next_gen.add(get_canonical(new_poly))
        poly_sets[n] = next_gen
        
    return poly_sets

def main():
    
    max_size = 5
    polyominoes = generate_polyominoes(max_size)
    
    print("Blokus Duo Piece Count Analysis")
    print("===============================")
    
    total_pieces = 0
    for n in range(1, max_size + 1):
        count = len(polyominoes[n])
        total_pieces += count
        print(f"Size n={n} (n-square pieces): {count} unique piece(s)")
        
    print("===============================")
    print(f"Total unique pieces in Blokus Duo: {total_pieces}")

if __name__ == "__main__":
    
    
    main()