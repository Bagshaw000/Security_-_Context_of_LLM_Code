import itertools

def count_combinations(num_bricks):
    
    orientations = 2
    
    rotations = 4
    
    single_brick_combinations = orientations * rotations
    
    
    total_combinations = single_brick_combinations ** num_bricks
    return total_combinations

def classify_combination(combination):
    
    
    if len(set(combination)) == 1:
        return 'Trivial'
    
    return 'Complicated'

def main():
    num_bricks = 6
    expected_combinations = 915103765
    actual_combinations = count_combinations(num_bricks)
    
    print(f"Expected: {expected_combinations}, Actual: {actual_combinations}")
    if actual_combinations == expected_combinations:
        print("LEGO's claim is verified.")
    else:
        print("LEGO's claim is not verified.")
    
    
    example_combinations = [
        ['A', 'A', 'A', 'A', 'A', 'A'],  
        ['A', 'B', 'A', 'B', 'A', 'B'],  
    ]
    
    for combo in example_combinations:
        print(f"Combination: {combo}, Classification: {classify_combination(combo)}")

main()