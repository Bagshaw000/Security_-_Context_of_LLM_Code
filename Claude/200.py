import itertools

def get_combinations(num_bricks, brick_size):
    bricks = [1] * brick_size
    combinations = list(itertools.product(bricks, repeat=num_bricks))
    return len(combinations)

def verify_lego_claim():
    num_bricks = 6
    brick_size = 4
    total_combinations = get_combinations(num_bricks, brick_size)
    print(f"Total combinations: {total_combinations}")
    if total_combinations == 915103765:
        print("LEGO's claim is verified.")
    else:
        print("LEGO's claim is not verified.")

def classify_combinations(num_bricks, brick_size):
    total_combinations = get_combinations(num_bricks, brick_size)
    trivial_threshold = 1000
    complicated_threshold = 100000

    trivial_count = 0
    complicated_count = 0

    for combination in itertools.product(range(brick_size), repeat=num_bricks):
        if sum(combination) == num_bricks * (brick_size - 1):
            trivial_count += 1
        elif sum(combination) > num_bricks * (brick_size - 2):
            complicated_count += 1

    print(f"Total combinations: {total_combinations}")
    print(f"Trivial combinations: {trivial_count} (Class A)")
    print(f"Complicated combinations: {complicated_count} (Class B)")
    print(f"Remaining combinations: {total_combinations - trivial_count - complicated_count} (Class C)")

verify_lego_claim()
classify_combinations(6, 4)