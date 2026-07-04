import itertools

def count_combinations(num_bricks, brick_size):
    
    return sum(1 for _ in itertools.product(range(brick_size[0]), repeat=num_bricks))

def classify_combinations(num_bricks, brick_size):
    
    total_combinations = count_combinations(num_bricks, brick_size)
    
    
    is_trivial = lambda arrangement: all(brick_size[0] - 1 >= sum(arrangement[i:i+brick_size[0]]) for i in range(0, len(arrangement), brick_size[0]))
    
    trivial_combinations = sum(1 for arrangement in itertools.product(range(brick_size[0]), repeat=num_bricks) if is_trivial(arrangement))
    complicated_combinations = total_combinations - trivial_combinations
    
    return {
        "trivial": trivial_combinations,
        "complicated": complicated_combinations
    }


num_bricks = 6
brick_size = (2, 4)

total_combinations = count_combinations(num_bricks, brick_size)
print(f"Total number of combinations: {total_combinations}")

combination_classes = classify_combinations(num_bricks, brick_size)
print(f"Trivial combinations: {combination_classes['trivial']}")
print(f"Complicated combinations: {combination_classes['complicated']}")