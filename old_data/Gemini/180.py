import unittest
from typing import Set, Tuple, List, Dict


Polyomino = Tuple[Tuple[int, int], ...]

def normalize(cells: List[Tuple[int, int]]) -> Polyomino:
    
    min_x = min(c[0] for c in cells)
    min_y = min(c[1] for c in cells)
    return tuple(sorted((c[0] - min_x, c[1] - min_y) for c in cells))

def get_all_symmetries(cells: List[Tuple[int, int]]) -> List[Polyomino]:
    
    symmetries = []
    current = cells
    for _ in range(4):
        
        current = [(c[1], -c[0]) for c in current]
        symmetries.append(normalize(current))
        
        reflected = [(-c[0], c[1]) for c in current]
        symmetries.append(normalize(reflected))
    return symmetries

def get_canonical_form(cells: List[Tuple[int, int]]) -> Polyomino:
    
    return min(get_all_symmetries(cells))

def calculate_blokus_pieces(max_n: int = 5) -> Dict[int, Set[Polyomino]]:
    
    
    pieces_by_size = {i: set() for i in range(1, max_n + 1)}
    
    
    monomino = ((0, 0),)
    pieces_by_size[1].add(monomino)

    
    for n in range(2, max_n + 1):
        for prev_piece in pieces_by_size[n - 1]:
            
            for x, y in prev_piece:
                
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in prev_piece:
                        
                        new_piece_cells = list(prev_piece) + [neighbor]
                        
                        pieces_by_size[n].add(get_canonical_form(new_piece_cells))
                        
    return pieces_by_size

class TestBlokusLogic(unittest.TestCase):
    
    def test_piece_counts(self):
        results = calculate_blokus_pieces(5)
        self.assertEqual(len(results[1]), 1, "Should be 1 monomino")
        self.assertEqual(len(results[2]), 1, "Should be 1 domino")
        self.assertEqual(len(results[3]), 2, "Should be 2 trominoes")
        self.assertEqual(len(results[4]), 5, "Should be 5 tetrominoes")
        self.assertEqual(len(results[5]), 12, "Should be 12 pentominoes")

def main():
    max_size = 5
    results = calculate_blokus_pieces(max_size)
    
    print(f"Blokus Duo Piece Count Analysis (n=1 to {max_size})")
    print("=" * 50)
    
    total_pieces = 0
    for n in range(1, max_size + 1):
        count = len(results[n])
        total_pieces += count
        print(f"Size {n} (n={n}): {count} unique piece(s)")
        
    print("-" * 50)
    print(f"Total unique pieces in Blokus Duo: {total_pieces}")
    print("=" * 50)

    
    print("\nRunning unit tests for verification...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBlokusLogic)
    unittest.TextTestRunner(verbosity=1).run(suite)

if __name__ == "__main__":
    main()