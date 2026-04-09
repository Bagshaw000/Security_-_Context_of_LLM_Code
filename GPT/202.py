from itertools import permutations

def generate_combinations(brick_count):
    
    return set(permutations(range(brick_count), brick_count))

def classify_combination(combination):
    
    if len(set(combination)) == len(combination):
        return 'trivial'
    else:
        return 'complicated'

def verify_legos_combinations(brick_count):
    combinations = generate_combinations(brick_count)
    trivial_count = 0
    complicated_count = 0

    for combination in combinations:
        if classify_combination(combination) == 'trivial':
            trivial_count += 1
        else:
            complicated_count += 1

    return len(combinations), trivial_count, complicated_count

brick_count = 6
total_combinations, trivial_count, complicated_count = verify_legos_combinations(brick_count)

print(f'Total combinations: {total_combinations}')
print(f'Trivial combinations: {trivial_count}')
print(f'Complicated combinations: {complicated_count}')
print(f'Claim verified: {total_combinations == 915103765}')