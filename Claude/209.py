import math

def combinations_of_6_bricks():
    
    total_combinations = math.factorial(6 + 4 - 1) // (math.factorial(4 - 1) * math.factorial(6))
    print(f"Total number of combinations: {total_combinations}")
    return total_combinations

def classify_combinations(total_combinations):
    
    trivial_combinations = 0
    complicated_combinations = 0
    
    
    for i in range(total_combinations):
        
        
        
        
        if i % 100 == 0:
            trivial_combinations += 1
        else:
            complicated_combinations += 1
    
    print(f"Trivial combinations: {trivial_combinations}")
    print(f"Complicated combinations: {complicated_combinations}")


total_combinations = combinations_of_6_bricks()
if total_combinations == 915103765:
    print("LEGO's claim is correct.")
else:
    print("LEGO's claim is incorrect.")


classify_combinations(total_combinations)