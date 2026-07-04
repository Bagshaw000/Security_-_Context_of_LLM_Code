from itertools import permutations

def count_combinations(num_bricks):
    
    orientations = 2 ** num_bricks
    
    positions = factorial(num_bricks + 1) // factorial(num_bricks - 1)
    return orientations * positions

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

def classify_combination(combination):
    
    if all(combination[i] == combination[i + 1] for i in range(len(combination) - 1)):
        return "trivial"
    return "complicated"

def main():
    num_bricks = 6
    expected_combinations = 915103765
    actual_combinations = count_combinations(num_bricks)
    
    print(f"Expected: {expected_combinations}, Actual: {actual_combinations}")
    print("Claim Verified!" if actual_combinations == expected_combinations else "Claim Not Verified!")
    
    
    example_combination = [1, 1, 1, 1, 1, 1]  
    print(f"Combination {example_combination} is {classify_combination(example_combination)}.")

if __name__ == "__main__":
    main()