





def calculate_height(x):
    return -(x - 5)**2 + 10



def calculate_slope(x):
    return -2 * (x - 5)


current_position = 0.0



step_size = 0.1



for attempt in range(100):
    
    slope_here = calculate_slope(current_position)
    
    
    
    
    current_position = current_position + (slope_here * step_size)


print("The computer has finished climbing.")
print("The highest position found is:")
print(current_position)

print("The height at that peak is:")
print(calculate_height(current_position))