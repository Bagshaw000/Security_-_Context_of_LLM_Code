import sys

def normalize(shape):
    
    min_x = min(p[0] for p in shape)
    min_y = min(p[1] for p in shape)
    return tuple(sorted((p[0] - min_x, p[1] - min_y) for p in shape))

def get_canonical_form(shape):
    
    def rotate_90(coords):
        return [(p[1], -p[0]) for p in coords]
    
    def reflect(coords):
        return [(p[0], -p[1]) for p in coords]

    symmetries = []
    current_rotation = list(shape)
    
    
    for _ in range(4):
        current_rotation = rotate_90(current_rotation)
        symmetries.append(normalize(current_rotation))
    
    