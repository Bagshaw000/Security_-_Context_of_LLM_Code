import itertools

def count_combinations(num_bricks, brick_size):
    
    return sum(1 for _ in itertools.product(range(brick_size[0]), range(brick_size[1]), repeat=num_bricks))

def classify_combinations(num_bricks, brick_size):
    
    total_combinations = count_combinations(num_bricks, brick_size)
    print(f"Total combinations: {total_combinations}")

    if total_combinations == 915103765:
        print("LEGO's claim is verified.")
    else:
        print("LEGO's claim is not verified.")

    
    unique_orientations = set(itertools.product(range(brick_size[0]), range(brick_size[1]), repeat=num_bricks))
    num_unique_orientations = len(unique_orientations)

    if num_unique_orientations == total_combinations:
        print("Class A: All combinations are unique and complicated.")
    elif num_unique_orientations > total_combinations // 2:
        print("Class B: Most combinations are unique and complicated.")
    else:
        print("Class C: Many combinations are trivial and repetitive.")


classify_combinations(6, (2, 4))