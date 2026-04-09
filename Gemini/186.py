from typing import Set, Tuple, List, Dict


Coord = Tuple[int, int]
Piece = Tuple[Coord, ...]

def normalize(coords: List[Coord]) -> Piece:
    
    min_x = min(p[0] for p in coords)
    min_y = min(p[1] for p in coords)
    return tuple(sorted((x - min_x, y - min_y) for x, y in coords))

def get_canonical_form(coords: List[Coord]) -> Piece:
    
    symmetries = []
    curr = coords
    for _ in range(4):
        
        curr = [(y, -x) for x, y in curr]
        symmetries.append(normalize(curr))
        
        flipped = [(x, -y) for x, y in curr]
        symmetries.append(normalize(flipped))
    return min(symmetries)

def generate_free_polyominoes(max_n: int) -> Dict[int, Set[Piece]]:
    
    
    polyominoes_by_size: Dict[int, Set[Piece]] = {1: {((0, 0),)}}

    for n in range(1, max_n):
        next_gen: Set[Piece] = set()
        for piece in polyominoes_by_size[n]:
            
            for x, y in piece:
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in piece:
                        new_piece_list = list(piece) + [(nx, ny)]
                        
                        canonical = get_canonical_form(new_piece_list)
                        next_gen.add(canonical)
        polyominoes_by_size[n + 1] = next_gen

    return polyominoes_by_size

def main():
    
    max_n = 5
    results = generate_free_polyominoes(max_n)
    
    print(f"{'n-Square':<10} | {'Unique Pieces':<15}")
    print("-" * 30)
    
    total_pieces = 0
    for n in range(1, max_n + 1):
        count = len(results[n])
        total_pieces += count
        print(f"{n:<10} | {count:<15}")
        
    print("-" * 30)
    print(f"Total unique pieces in Blokus Duo: {total_pieces}")

if __name__ == "__main__":
    main()