def get_canonical_form(shape):
    
    def normalize(coords):
        min_x = min(p[0] for p in coords)
        min_y = min(p[1] for p in coords)
        return tuple(sorted((p[0] - min_x, p[1] - min_y) for p in coords))

    def rotate_90(coords):
        return [(p[1], -p[0]) for p in coords]

    def reflect(coords):
        return [(p[0], -p[1]) for p in coords]

    symmetries = []
    current_shape = list(shape)
    for _ in range(4):
        symmetries.append(normalize(current_shape))
        symmetries.append(normalize(reflect(current_shape)))
        current_shape = rotate_90(current_shape)
    
    return min(symmetries)

def calculate_blokus_pieces(max_n=5):
    
    
