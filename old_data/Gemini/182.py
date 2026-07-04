import collections

def normalize(polyomino):
    
    min_x = min(p[0] for p in polyomino)
    min_y = min(p[1] for p in polyomino)
    return tuple(sorted((x - min_x, y - min_y) for x, y in polyomino))

def get_symmetries(polyomino):
    
    symmetries = []
    current = list(polyomino)
    for _ in range(4):
        
        current = [(p[1], -p[0]) for p in current]
        symmetries.append(normalize(current))
        
        reflected = [(p[0], -p[1]) for p in current]
        symmetries.append(normalize(reflected))
    return set(symmetries)

def generate_free_polyominoes(max_n):
    
    
    polyominoes_by_size = collections.defaultdict(set)
    
    
    monomino = ((0, 0),)
    polyominoes_by_size[1].add(monomino)
    
    
    for n in range(2, max_n + 1):
        for prev_poly in polyominoes_by_size[n-1]:
            for x, y in prev_poly:
                
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in prev_poly:
                        
                        candidate = list(prev_poly)
                        candidate.append(neighbor)
                        normalized_candidate = normalize(candidate)
                        
                        
                        symmetries = get_symmetries(normalized_candidate)
                        if not any(sym in polyominoes_by_size[n] for sym in symmetries):
                            polyominoes_by_size[n].add(normalized_candidate)
                            
    return polyominoes_by_size

def run_blokus_analysis():
    
    max_n = 5
    results = generate_free_polyominoes(max_n)
    
    print(f"{'n-Squares':<12} | {'Unique Pieces (Possibilities)':<30}")
    print("-" * 45)
    
    total_pieces = 0
    for n in range(1, max_n + 1):
        count = len(results[n])
        print(f"{n:<12} | {count:<30}")
        total_pieces += count
        
    print("-" * 45)
    print(f"Total unique pieces in Blokus Duo: {total_pieces}")

def test_logic():
    
    expected = {1: 1, 2: 1, 3: 2, 4: 5, 5: 12}
    actual_data = generate_free_polyominoes(5)
    for n, count in expected.items():
        assert len(actual_data[n]) == count, f"Failure at n={n}"
    print("\nUnit test passed: Polyomino counts match mathematical constants.")

if __name__ == "__main__":
    run_blokus_analysis()
    test_logic()