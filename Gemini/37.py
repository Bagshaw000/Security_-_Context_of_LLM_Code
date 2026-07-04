def normalize_polyomino(coords):
    
    def get_all_variants(pts):
        for _ in range(4):
            
            min_x = min(p[0] for p in pts)
            min_y = min(p[1] for p in pts)
            yield tuple(sorted((p[0] - min_x, p[1] - min_y) for p in pts))
            
            
            reflected = [(p[0], -p[1]) for p in pts]
            min_rx = min(p[0] for p in reflected)
            min_ry = min(p[1] for p in reflected)
            yield tuple(sorted((p[0] - min_rx, p[1] - min_ry) for p in reflected))
            
            
            pts = [(-p[1], p[0]) for p in pts]

    
    return min(get_all_variants(coords))

def generate_free_polyominoes(max_n):
    
    
    polyominoes_by_size = {1: {((0, 0),)}}
    
    for n in range(2, max_n + 1):
        new_set = set()
        for poly in polyominoes_by_size[n-1]:
            
            for x, y in poly:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in poly:
                        
                        candidate = list(poly) + [neighbor]
                        new_set.add(normalize_polyomino(candidate))
        polyominoes_by_size[n] = new_set
        
    return polyominoes_by_size

def main():
    
    
    max_n = 5
    results = generate_free_polyominoes(max_n)
    
    print(f"{'n-size':<10} | {'Unique Pieces (Possibilities)':<15}")
    print("-" * 40)
    
    total_pieces = 0
    for n in range(1, max_n + 1):
        count = len(results[n])
        print(f"{n:<10} | {count:<15}")
        total_pieces += count
        
    print("-" * 40)
    print(f"Total Blokus Duo pieces: {total_pieces}")

if __name__ == "__main__":
    main()