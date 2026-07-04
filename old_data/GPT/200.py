import itertools

def count_combinations(num_bricks):
    
    orientations = 2
    
    positions = 6
    
    total_combinations = orientations ** num_bricks * factorial(num_bricks)
    return total_combinations

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def classify_combination(combination):
    
    if all(combination[i] == combination[i + 1] for i in range(len(combination) - 1)):
        return "Trivial"
    else:
        return "Complicated"

def main():
    num_bricks = 6
    claimed_combinations = 915103765
    actual_combinations = count_combinations(num_bricks)

    print(f"Claimed combinations: {claimed_combinations}")
    print(f"Actual combinations: {actual_combinations}")
    print("Claim verified:", claimed_combinations == actual_combinations)

    
    example_combinations = [
        [1, 1, 1, 1, 1, 1],  
        [1, 2, 1, 2, 1, 2],  
    ]

    for combo in example_combinations:
        print(f"Combination: {combo}, Classification: {classify_combination(combo)}")

main()