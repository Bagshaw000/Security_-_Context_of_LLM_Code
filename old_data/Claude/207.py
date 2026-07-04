import itertools

def count_combinations(n_bricks, brick_size):
    
    return sum(1 for _ in itertools.product(range(2), repeat=n_bricks * brick_size))

def classify_combinations(n_bricks, brick_size):
    
    total_combinations = count_combinations(n_bricks, brick_size)
    print(f"Total number of combinations: {total_combinations}")

    if total_combinations == 915103765:
        print("LEGO's claim is verified.")
    else:
        print("LEGO's claim is not verified.")

    
    trivial_threshold = 10
    complicated_threshold = 100

    trivial_count = 0
    complicated_count = 0

    for combo in itertools.product(range(2), repeat=n_bricks * brick_size):
        
        max_consecutive = 0
        current_streak = 1
        for i in range(1, len(combo)):
            if combo[i] == combo[i-1]:
                current_streak += 1
            else:
                max_consecutive = max(max_consecutive, current_streak)
                current_streak = 1
        max_consecutive = max(max_consecutive, current_streak)

        if max_consecutive <= trivial_threshold:
            trivial_count += 1
        elif max_consecutive >= complicated_threshold:
            complicated_count += 1

    print(f"Trivial combinations: {trivial_count}")
    print(f"Complicated combinations: {complicated_count}")


classify_combinations(6, 8)