import itertools

def count_combinations(num_bricks):
    
    orientations = 2
    
    rotations = 4
    
    total_combinations = orientations * rotations ** (num_bricks - 1)
    return total_combinations

def classify_combination(combination):
    
    
    if all(brick == combination[0] for brick in combination):
        return 'Trivial'
    else:
        return 'Complicated'

def main():
    num_bricks = 6
    expected_combinations = 915103765
    actual_combinations = count_combinations(num_bricks)

    print(f"Expected Combinations: {expected_combinations}")
    print(f"Actual Combinations: {actual_combinations}")
    
    if actual_combinations == expected_combinations:
        print("LEGO's claim is verified.")
    else:
        print("LEGO's claim is not verified.")

    
    example_combinations = [
        ['up', 'up', 'up', 'up', 'up', 'up'],
        ['up', 'down', 'up', 'up', 'down', 'up'],
        ['down', 'down', 'down', 'down', 'down', 'down']
    ]

    for combo in example_combinations:
        rating = classify_combination(combo)
        print(f"Combination: {combo} is classified as {rating}")

main()