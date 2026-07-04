import itertools

def count_combinations(num_bricks):
    
    orientations = 2 ** num_bricks
    
    positions = 6 ** num_bricks
    
    total_combinations = orientations * positions
    return total_combinations

def classify_combination(combination):
    
    if len(set(combination)) > 3:
        return 'Complicated'
    return 'Trivial'

def main():
    num_bricks = 6
    total_combinations = count_combinations(num_bricks)
    print(f'Total combinations for {num_bricks} bricks: {total_combinations}')
    
    
    lego_claim = 915103765
    if total_combinations == lego_claim:
        print("LEGO's claim is verified.")
    else:
        print("LEGO's claim is not verified.")
    
    
    example_combinations = [
        (1, 2, 3, 4, 5, 6),
        (1, 1, 2, 2, 3, 3),
        (1, 1, 1, 1, 1, 1),
        (1, 2, 3, 4, 5, 6, 7)
    ]
    
    for combo in example_combinations:
        rating = classify_combination(combo)
        print(f'Combination {combo} is classified as: {rating}')

main()