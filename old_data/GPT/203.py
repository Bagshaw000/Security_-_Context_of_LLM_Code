import itertools

def count_combinations(num_bricks):
    
    orientations = 2 ** num_bricks
    
    positions = 4 ** num_bricks
    
    total_combinations = orientations * positions
    return total_combinations

def classify_combination(combination):
    
    if all(combination[i][0] == combination[0][0] for i in range(len(combination))):
        return 'trivial'
    else:
        return 'complicated'

def main():
    num_bricks = 6
    total_combinations = count_combinations(num_bricks)
    print(f'Total combinations for {num_bricks} bricks: {total_combinations}')
    
    
    example_combinations = [
        [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)],  
        [(0, 0), (1, 1), (0, 2), (1, 3), (0, 4), (1, 5)]   
    ]
    
    for combo in example_combinations:
        rating = classify_combination(combo)
        print(f'Combination {combo} is classified as: {rating}')

main()