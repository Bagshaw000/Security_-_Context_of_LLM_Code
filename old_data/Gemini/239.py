import random







def mathematical_formula(x):
    
    return -(x**4) + 10*(x**2) + 2*x



def calculate_slope(x):
    return -4*(x**3) + 20*x + 2




best_position_found = 0
highest_value_found = -float('inf')


for trial in range(20):
    
    current_x = random.uniform(-5, 5)
    
    
    
    for step in range(100):
        
        slope = calculate_slope(current_x)
        
        
        
        current_x = current_x + (0.01 * slope)
            
    
    current_value = mathematical_formula(current_x)
    if current_value > highest_value_found:
        highest_value_found = current_value
        best_position_found = current_x


print("Search complete.")
print("The highest peak (Global Maximum) is located at x =")
print(best_position_found)
print("The height of the curve at this peak is =")
print(highest_value_found)