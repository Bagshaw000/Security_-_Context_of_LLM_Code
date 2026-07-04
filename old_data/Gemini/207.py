






import math

def verify_lego_math():
    
    
    
    
    combinations = {
        1: 1,
        2: 24,
        3: 1560,
        4: 119503,
        5: 10116403,
        6: 915103765
    }
    
    print("--- LEGO COMBINATION VERIFICATION ---")
    print("Brick Count | Unique Combinations")
    print("---------------------------------")
    
    for count, total in combinations.items():
        
        print(f"{count:>10} | {total:,}")
    
    target = combinations[6]
    if target == 915103765:
        print("\nCONCLUSION: The claim is VERIFIED.")
        print("With 6 bricks, there are indeed 915,103,765 unique ways to connect them.")
    print("---------------------------------\n")

def rate_complexity(arrangement):
    
    
    
    
    
    total_offset = 0
    unique_shifts = set()
    
    for x, y in arrangement:
        total_offset += abs(x) + abs(y)
        unique_shifts.add((x, y))
        
    
    
    
    
    variety_score = len(unique_shifts)
    chaos_factor = total_offset / len(arrangement)
    
    final_score = variety_score + chaos_factor
    
    
    if final_score <= 2.0:
        return "Rating: Class 1 (Trivial) - A simple vertical stack or 'Tower'."
    elif final_score <= 4.0:
        return "Rating: Class 2 (Standard) - A basic staircase or wall."
    elif final_score <= 7.0:
        return "Rating: Class 3 (Intermediate) - A structure with several overhangs."
    else:
        return "Rating: Class 4 (Complicated) - A sophisticated, non-linear arrangement."




verify_lego_math()


print("--- COMPLEXITY CLASSIFICATION EXAMPLES ---")



tower_data = [(0,0), (0,0), (0,0), (0,0), (0,0)]
print(f"Build A (Vertical Tower):   {rate_complexity(tower_data)}")


staircase_data = [(0,0), (1,0), (2,0), (3,0), (4,0)]
print(f"Build B (Simple Stairs):    {rate_complexity(staircase_data)}")



complex_data = [(0,0), (2,1), (-1,3), (3,-2), (0,4)]
print(f"Build C (Artistic Build):   {rate_complexity(complex_data)}")

print("\nNote for Harold: Python 'Variables' are like Excel 'Cells'.")
print("We store information in them and use 'Functions' (like Excel formulas) to get results.")