





def calculate_height(x):
    
    
    return -(x - 10)**2 + 50



def calculate_slope(x):
    
    return -2 * (x - 10)



current_position = 0



learning_rate = 0.1


total_steps = 50

print("Beginning the climb to find the highest point...")



for step_number in range(1, total_steps + 1):
    
    slope = calculate_slope(current_position)
    
    
    
    current_position = current_position + (slope * learning_rate)
    
    
    if step_number % 10 == 0:
        current_height = calculate_height(current_position)
        print("Step " + str(step_number) + ": Checking position " + str(round(current_position, 2)) + "... Current height is " + str(round(current_height, 2)))


final_height = calculate_height(current_position)
print("\nSearch Finished!")
print("The highest point found is at x = " + str(round(current_position, 2)))
print("The maximum height reached is " + str(round(final_height, 2)))



