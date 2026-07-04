import itertools

def count_combinations(brick_count):
    
    orientations = 2
    
    positions = 8
    
    total_combinations = orientations ** brick_count * positions ** brick_count
    return total_combinations

def classify_combination(combination):
    
    
    if len(set(combination)) == 1:
        return 'Trivial'
    
    return 'Complicated'

def main():
    brick_count = 6
    total_combinations = count_combinations(brick_count)
    print(f'Total combinations for {brick_count} bricks: {total_combinations}')
    
    
    lego_claim = 915103765
    if total_combinations == lego_claim:
        print("LEGO's claim is verified.")
    else:
        print("LEGO's claim is not verified.")
    
    
    example_combinations = [
        ['A', 'A', 'A', 'A', 'A', 'A'],  
        ['A', 'B', 'A', 'B', 'A', 'B'],  
        ['C', 'C', 'C', 'C', 'C', 'C']   
    ]
    
    for combo in example_combinations:
        rating = classify_combination(combo)
        print(f'Combination {combo} is classified as: {rating}')

main()