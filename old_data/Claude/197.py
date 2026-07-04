import itertools

def verify_lego_combinations():
    bricks = [1, 1, 1, 1, 1, 1]
    combinations = list(itertools.permutations(bricks, 6))
    return len(set(combinations))

def classify_combinations():
    bricks = [1, 1, 1, 1, 1, 1]
    combinations = list(itertools.permutations(bricks, 6))
    classes = {}
    for combo in combinations:
        num_unique = len(set(combo))
        if num_unique == 1:
            class_rating = 'trivial'
        elif num_unique == 2:
            class_rating = 'simple'
        elif num_unique == 3:
            class_rating = 'moderate'
        else:
            class_rating = 'complicated'
        if class_rating not in classes:
            classes[class_rating] = 0
        classes[class_rating] += 1
    return classes