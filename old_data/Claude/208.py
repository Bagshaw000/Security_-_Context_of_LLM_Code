import itertools

def count_combinations(bricks):
    
    return sum(len(list(itertools.combinations(range(bricks), i))) for i in range(1, bricks+1))

def classify_combinations(bricks):
    
    combinations = {}
    for i in range(1, bricks+1):
        for combo in itertools.combinations(range(bricks), i):
            key = ''.join(map(str, combo))
            complexity = sum(abs(x-y) for x, y in zip(combo, combo[1:]))
            if complexity <= 2:
                combinations[key] = 'Trivial'
            elif complexity <= 4:
                combinations[key] = 'Simple'
            elif complexity <= 6:
                combinations[key] = 'Moderate'
            else:
                combinations[key] = 'Complicated'
    return combinations


num_bricks = 6
total_combinations = count_combinations(num_bricks)
print(f"LEGO claims that {num_bricks} standard 2X4 bricks can be connected in {915103765} combinations.")
print(f"The code verifies that there are {total_combinations} possible combinations.")

combination_classes = classify_combinations(num_bricks)
print("Combination classification:")
for combo, class_name in combination_classes.items():
    print(f"{combo}: {class_name}")