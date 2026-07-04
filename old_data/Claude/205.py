import itertools

def verify_lego_combinations():
    bricks = [0, 1, 2, 3, 4, 5]
    combinations = list(itertools.permutations(bricks, 6))
    total_combinations = len(combinations)
    print(f"Total combinations: {total_combinations}")
    return total_combinations

def classify_combinations(combinations):
    trivial_combinations = 0
    complicated_combinations = 0
    for combination in combinations:
        unique_bricks = len(set(combination))
        if unique_bricks == 6:
            complicated_combinations += 1
        else:
            trivial_combinations += 1
    print(f"Trivial combinations: {trivial_combinations}")
    print(f"Complicated combinations: {complicated_combinations}")

total_combinations = verify_lego_combinations()
if total_combinations == 915103765:
    print("LEGO's claim is correct.")
else:
    print("LEGO's claim is incorrect.")

combinations = list(itertools.permutations([0, 1, 2, 3, 4, 5], 6))
classify_combinations(combinations)