Here's the Python code that verifies the LEGO claim and designs a heuristic to classify the combinations:

import itertools

def count_combinations(num_bricks, brick_size):
    
    total_combinations = 0
    for i in range(1, num_bricks + 1):
        combinations = itertools.combinations(range(num_bricks), i)
        for combination in combinations:
            total_length = sum(brick_size[0] for index in combination)
            total_width = max(brick_size[1] for index in combination)
            if total_length <= 8 and total_width <= 4:
                total_combinations += 1
    return total_combinations


num_bricks = 6
brick_size = (2, 4)
total_combinations = count_combinations(num_bricks, brick_size)
print(f"Total number of combinations: {total_combinations}")
if total_combinations == 915103765:
    print("LEGO claim is verified.")
else:
    print("LEGO claim is not verified.")

def classify_combination(brick_indices):
    
    total_length = sum(2 for index in brick_indices)
    total_width = max(4 for index in brick_indices)
    if total_length <= 4 and total_width <= 4:
        return "Class A"
    elif total_length <= 6 and total_width <= 4:
        return "Class B"
    else:
        return "Class C"