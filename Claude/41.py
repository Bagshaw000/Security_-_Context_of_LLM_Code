import itertools

def verify_lego_combinations():
    bricks = [1, 1, 1, 1, 1, 1]
    combinations = list(itertools.permutations(bricks, 6))
    total_combinations = len(combinations)
    print(f"Total combinations: {total_combinations}")
    return total_combinations

def classify_combinations(total_combinations):
    trivial_threshold = 10
    complicated_threshold = 100
    
    trivial_count = 0
    complicated_count = 0
    
    for combination in range(total_combinations):
        if combination < trivial_threshold:
            trivial_count += 1
        elif combination < complicated_threshold:
            complicated_count += 1
    
    print(f"Trivial combinations: {trivial_count}")
    print(f"Complicated combinations: {complicated_count}")

total_combinations = verify_lego_combinations()
classify_combinations(total_combinations)