import itertools

def count_combinations(num_bricks):
    
    orientations = 2
    
    positions = 4
    
    total_combinations = orientations * positions ** (num_bricks - 1)
    return total_combinations

def classify_combination(combination):
    
    
    if all(combination[i][0] == combination[0][0] for i in range(len(combination))):
        return "Trivial"
    else:
        return "Complicated"

def main():
    num_bricks = 6
    expected_combinations = 915103765
    actual_combinations = count_combinations(num_bricks)

    print(f"Expected: {expected_combinations}, Actual: {actual_combinations}")
    assert actual_combinations == expected_combinations, "Combination count does not match!"

    
    example_combinations = [
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)],  
        [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],  
    ]

    for combo in example_combinations:
        classification = classify_combination(combo)
        print(f"Combination: {combo}, Classification: {classification}")

main()