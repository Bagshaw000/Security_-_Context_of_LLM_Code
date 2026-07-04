import itertools

def count_brick_combinations():
    bricks = [1, 1, 1, 1, 1, 1]
    total_combinations = 0
    for i in range(1, len(bricks) + 1):
        combinations = itertools.combinations(bricks, i)
        total_combinations += len(list(combinations))
    return total_combinations

def classify_combinations():
    bricks = [1, 1, 1, 1, 1, 1]
    combinations = []
    for i in range(1, len(bricks) + 1):
        combinations.extend(list(itertools.combinations(bricks, i)))
    
    trivial_count = 0
    complicated_count = 0
    
    for combination in combinations:
        if sum(combination) == len(combination):
            trivial_count += 1
        else:
            complicated_count += 1
    
    print(f"Trivial combinations: {trivial_count}")
    print(f"Complicated combinations: {complicated_count}")

print(count_brick_combinations())
classify_combinations()