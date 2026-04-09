import itertools

def verify_lego_claim():
    bricks = [1, 1, 1, 1, 1, 1]
    combinations = list(itertools.permutations(bricks, 6))
    return len(set(combinations))

def classify_combinations():
    bricks = [1, 1, 1, 1, 1, 1]
    combinations = list(itertools.permutations(bricks, 6))
    class_ratings = {}
    for combo in combinations:
        complexity = sum(abs(combo[i] - combo[i-1]) for i in range(1, 6))
        if complexity <= 2:
            class_rating = 'trivial'
        elif complexity <= 5:
            class_rating = 'moderate'
        else:
            class_rating = 'complicated'
        class_ratings[combo] = class_rating
    return class_ratings