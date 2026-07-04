






def find_height_at(position):
    
    return -(position - 5)**2 + 10




def find_steepness_at(position):
    
    return -2 * (position - 5)


current_position = 0.0    
step_size = 0.1           
number_of_tries = 100     

print("Starting the climb at position 0...")



for attempt in range(number_of_tries):
    
    slope = find_steepness_at(current_position)
    
    
    
    
    current_position = current_position + (slope * step_size)
    
    
    if attempt % 10 == 0:
        current_height = find_height_at(current_position)
        print("After " + str(attempt) + " steps, we are at position " + str(round(current_position, 2)))


final_height = find_height_at(current_position)

print("----------------------------------------------")
print("The computer has finished climbing the hill!")
print("The highest point found is at position: " + str(round(current_position, 2)))
print("The height at that peak is: " + str(round(final_height, 2)))
