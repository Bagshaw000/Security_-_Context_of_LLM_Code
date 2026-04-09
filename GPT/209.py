import itertools

def count_combinations(num_bricks):
    
    orientations = 2
    
    rotations = 4
    
    total_combinations = orientations * rotations ** (num_bricks - 1)
    return total_combinations

def classify_combination(combination):
    
    
    if all(combination[i][0] == combination[i + 1][0] for i in range(len(combination) - 1)):
        return 'Trivial'
    else:
        return 'Complicated'

def main():
    num_bricks = 6
    claimed_combinations = 915103765
    actual_combinations = count_combinations(num_bricks)

    print(f"Claimed combinations: {claimed_combinations}")
    print(f"Actual combinations: {actual_combinations}")
    print("Claim verified:", claimed_combinations == actual_combinations)

    
    example_combinations = [
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)],  
        [(0, 0), (1, 1), (0, 2), (1, 3), (0, 4), (1, 5)],  
    ]

    for combo in example_combinations:
        print(f"Combination: {combo}, Classification: {classify_combination(combo)}")

main()