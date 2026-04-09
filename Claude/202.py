import itertools

def lego_combinations(num_bricks, brick_size):
    total_combinations = 0
    for i in range(1, num_bricks + 1):
        combinations = list(itertools.combinations(range(num_bricks), i))
        total_combinations += len(combinations)
    return total_combinations

def classify_combinations(num_bricks, brick_size):
    total_combinations = lego_combinations(num_bricks, brick_size)
    print(f"Total combinations: {total_combinations}")
    
    trivial_threshold = 10
    complicated_threshold = 100
    
    trivial_count = 0
    complicated_count = 0
    
    for i in range(1, num_bricks + 1):
        combinations = list(itertools.combinations(range(num_bricks), i))
        for combo in combinations:
            if len(combo) <= trivial_threshold:
                trivial_count += 1
            elif len(combo) >= complicated_threshold:
                complicated_count += 1
    
    print(f"Trivial combinations: {trivial_count}")
    print(f"Complicated combinations: {complicated_count}")


num_bricks = 6
brick_size = 2
classify_combinations(num_bricks, brick_size)