




def function_to_climb(x):
    return -(x**2) + (4 * x) + 10




def get_slope(x):
    return -2 * x + 4



current_position = -10.0   
step_size = 0.1            
iterations = 60            

print("Starting the search for the highest point...")
print("---------------------------------------------")




for i in range(iterations):
    
    slope_at_this_spot = get_slope(current_position)
    
    
    
    current_position = current_position + (slope_at_this_spot * step_size)
    
    
    if i % 10 == 0:
        current_height = function_to_climb(current_position)
        print("Step " + str(i) + ": Current position is " + str(round(current_position, 2)) + ", Height is " + str(round(current_height, 2)))


final_height = function_to_climb(current_position)
print("---------------------------------------------")
print("Search complete!")
print("The highest point is at position: " + str(round(current_position, 4)))
print("The maximum value (the peak) is: " + str(round(final_height, 4)))





