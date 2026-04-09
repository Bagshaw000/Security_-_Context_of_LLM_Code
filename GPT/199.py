import itertools

def count_combinations():
    
    orientations = 2
    
    positions = 6
    
    total_combinations = orientations ** 6 * positions ** 6
    return total_combinations

def classify_combination(combination):
    
    orientations = [brick[1] for brick in combination]
    if len(set(orientations)) == 1:
        return 'trivial'
    else:
        return 'complicated'

def generate_combinations():
    bricks = list(itertools.product(range(1, 7), repeat=6))  
    combinations = []
    for brick_combination in bricks:
        for orientation in itertools.product([0, 1], repeat=6):  
            combination = list(zip(brick_combination, orientation))
            combinations.append(combination)
    return combinations

def main():
    total_combinations = count_combinations()
    print(f"Total combinations calculated: {total_combinations}")
    
    combinations = generate_combinations()
    trivial_count = sum(1 for combo in combinations if classify_combination(combo) == 'trivial')
    complicated_count = len(combinations) - trivial_count
    
    print(f"Trivial combinations: {trivial_count}")
    print(f"Complicated combinations: {complicated_count}")

main()