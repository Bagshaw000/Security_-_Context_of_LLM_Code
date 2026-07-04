import collections

def get_canonical(polyomino):
    
    variants = []
    coords = list(polyomino)
    
    for _ in range(4):
        
        coords = [(y, -x) for x, y in coords]
        for flip in [True, False]:
            if flip:
                
                test_coords = [(-x, y) for x, y in coords]
            else:
                test_coords = list(coords)
            
            
            min_x = min(c[0] for c in test_coords)
            min_y = min(c[1] for c in test_coords)
            normalized = sorted((c[0] - min_x, c[1] - min_y) for c in test_coords)
            variants.append(tuple(normalized))
            
    return min(variants)

def generate_free_polyominoes(max_n):
    
    
    polyominoes = {i: set() for i in range(1, max_n + 1)}
    
    
    monomino = ((0, 0),)
    polyominoes[1].add(monomino)
    
    for n in range(1, max_n):
        for poly in polyominoes[n]:
            
            for x, y in poly:
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_square = (x + dx, y + dy)
                    if new_square not in poly:
                        
                        new_poly = poly + (new_square,)
                        canonical = get_canonical(new_poly)
                        polyominoes[n + 1].add(canonical)
    
    return polyominoes

def main():
    
    max_size = 5
    all_pieces = generate_free_polyominoes(max_size)
    
    total_count = 0
    print(f"{'Size (n)':<10} | {'Unique Pieces':<15}")
    print("-" * 30)
    
    for n in range(1, max_size + 1):
        count = len(all_pieces[n])
        total_count += count
        print(f"{n:<10} | {count:<15}")
        
    print("-" * 30)
    print(f"Total pieces in Blokus Duo: {total_count}")

if __name__ == "__main__":
    main()