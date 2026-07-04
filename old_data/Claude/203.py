import itertools

def get_combinations(bricks):
    return len(list(itertools.product([0, 1], repeat=len(bricks))))

def classify_combinations(bricks):
    combinations = get_combinations(bricks)
    if combinations == 915103765:
        print(f"LEGO's claim of {combinations} combinations is correct.")
    else:
        print(f"LEGO's claim of {combinations} combinations is incorrect. The actual number of combinations is {get_combinations(bricks)}.")

    
    for i in range(len(bricks)):
        if sum(bricks[:i+1]) <= 4:
            print(f"Combination with first {i+1} bricks is trivial (Class 1)")
        else:
            print(f"Combination with first {i+1} bricks is complicated (Class 2)")

classify_combinations([1, 1, 1, 1, 1, 1])