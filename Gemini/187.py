from typing import Set, Tuple, List, Dict

def get_canonical_form(polyomino: Tuple[Tuple[int, int], ...]) -> Tuple[Tuple[int, int], ...]:
    
    def normalize(coords: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
        min_x = min(p[0] for p in coords)
        min_y = min(p[1] for p in coords)
        return tuple(sorted((p[0] - min_x, p[1] - min_y) for p in coords))

    def rotate(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        return [(p[1], -p[0]) for p in coords]

    def reflect(coords: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        return [(p[0], -p[1]) for p in coords]

    variants = []
    current = list(polyomino)
    for _ in range(4):
        variants.append(normalize(current))
        variants.append(normalize(reflect(current)))
        current = rotate(current)
    return min(variants)

def generate_polyominoes(max_n: int) -> Dict[int, Set[Tuple[Tuple[int, int], ...]]]:
    
    
    results