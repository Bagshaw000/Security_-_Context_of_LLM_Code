def get_canonical_form(coords):
    
    transformations = [
        lambda x, y: (x, y),
        lambda x, y: (y, -x),
        lambda x, y: (-x, -y),
        lambda x, y: (-y, x),
        lambda x, y: (x, -y),
        lambda x, y: (-y, -x),
        lambda x, y: (-x, y),
        lambda x, y: (y, x),
    ]
    
    forms = []
    for t in transformations:
        transformed = [t(x, y) for x, y in coords]
        min_x = min(p[0] for p in transformed)
        min_y = min(p[1] for p in transformed)
        normalized = sorted((x - min_x, y - min_y) for x, y in transformed)
        forms.append(tuple(normalized))
        
    return min(forms)

def find_all_polyominoes(max_n):
    
    poly_sets = {i: set() for i in range(1, max_n + 1)}
    poly_sets[1].add(((0, 0),))
    
    for n in range(1, max_n):
        for poly in poly_sets[n]:
            for x, y in poly:
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (x + dx, y + dy)
                    if neighbor not in poly:
                        new_poly = poly + (neighbor,)
                        poly_sets[n + 1].add(get_canonical_form(new_poly))
    return poly_sets

def main():
    
    
    max_n = 5
    polyominoes = find_all_polyominoes(max_n)
    
    print(f"{'n-square':<10} | {'Unique Pieces':<15}")
    print("-" * 30)
    
    total_pieces = 0
    for n in range