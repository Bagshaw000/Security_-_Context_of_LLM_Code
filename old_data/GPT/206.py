from itertools import permutations

def generate_combinations(brick_count):
    
    return set(permutations(range(brick_count), brick_count))

def classify_combination(combination):
    
    unique_bricks = len(set(combination))
    if unique_bricks == 1:
        return 'trivial'
    elif unique_bricks <= 3:
        return 'simple'
    else:
        return 'complicated'

def verify_legos_combinations(brick_count):
    combinations = generate_combinations(brick_count)
    total_combinations = len(combinations)
    
    trivial_count = 0
    simple_count = 0
    complicated_count = 0
    
    for combination in combinations:
        classification = classify_combination(combination)
        if classification == 'trivial':
            trivial_count += 1
        elif classification == 'simple':
            simple_count += 1
        else:
            complicated_count += 1
            
    return total_combinations, trivial_count, simple_count, complicated_count

brick_count = 6
total_combinations, trivial_count, simple_count, complicated_count = verify_legos_combinations(brick_count)

print(f'Total combinations: {total_combinations}')
print(f'Trivial combinations: {trivial_count}')
print(f'Simple combinations: {simple_count}')
print(f'Complicated combinations: {complicated_count}')