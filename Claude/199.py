import itertools

def count_brick_combinations():
    bricks = [1, 1, 1, 1, 1, 1]
    combinations = list(itertools.product(bricks, repeat=6))
    return len(combinations)

def classify_combinations():
    bricks = [1, 1, 1, 1, 1, 1]
    combinations = list(itertools.product(bricks, repeat=6))
    
    trivial = 0
    complicated = 0
    
    for combo in combinations:
        if sum(combo) == 6 or sum(combo) == 12:
            trivial += 1
        else:
            complicated += 1
    
    return (trivial, complicated)