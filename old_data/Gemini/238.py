




def get_height(x):
    
    
    return 1000 - (x - 50) * (x - 50)



def get_slope(x):
    
    return -2 * (x - 50)



current_guess = 0



step_size = 0.1


number_of_tries = 100

print("Starting the search at position 0...")



for count in range(number_of_tries):
    
    slope = get_slope(current_guess)
    
    
    
    current_guess = current_guess + (step_size * slope)
    
    
    if count % 10 == 0:
        height = get_height(current_guess)
        print("Try number:", count, " | Current Position:", round(current_guess, 2), " | Current Height:", round(height, 2))


final_height = get_height(current_guess)
print("--------------------------------------------------")
print("The search is finished.")
print("The best position found (the peak) is approximately:", round(current_guess, 2))
print("The maximum height reached at that peak is:", round(final_height, 2))