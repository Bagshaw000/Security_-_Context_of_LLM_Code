import itertools

def count_combinations(num_bricks):
    
    orientations = 2
    
    positions = 6
    
    total_combinations = orientations ** num_bricks * positions ** num_bricks
    return total_combinations

def classify_combination(combination):
    
    if len(combination) < 3:
        return "Trivial"
    elif len(combination) < 6:
        return "Moderate"
    else:
        return "Complicated"


num_bricks = 6
calculated_combinations = count_combinations(num_bricks)
lego_claim = 915103765

print("Calculated Combinations:", calculated_combinations)
print("LEGO Claim:", lego_claim)
print("Claim Verified:", calculated_combinations == lego_claim)


example_combinations = [
    ['A', 'B'],  
    ['A', 'B', 'C', 'D'],  
    ['A', 'B', 'C', 'D', 'E', 'F', 'G']  
]

for combo in example_combinations:
    print(f"Combination: {combo}, Classification: {classify_combination(combo)}")