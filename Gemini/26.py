



lift_A_location = 1
lift_B_location = 1


for turn in range(3):
    print("-------------------------------------------")
    print("Lift A is currently at floor:", lift_A_location)
    print("Lift B is currently at floor:", lift_B_location)
    
    
    
    your_floor = int(input("Which floor are you standing on? (1 to 10): "))
    
    
    
    distance_to_A = abs(lift_A_location - your_floor)
    distance_to_B = abs(lift_B_location - your_floor)
    
    
    if distance_to_A <= distance_to_B:
        print("Sending Lift A to pick you up...")
        lift_A_location = your_floor
        chosen_lift = "A"
    else:
        print("Sending Lift B to pick you up...")
        lift_B_location = your_floor
        chosen_lift = "B"
        
    
    destination = int(input("You are now in the lift. Which floor do you want to go to? "))
    
    
    if chosen_lift == "A":
        lift_A_location = destination
        print("Lift A is moving... arrived at floor", lift_A_location)
    else:
        lift_B_location = destination
        print("Lift B is moving... arrived at floor", lift_B_location)

print("-------------------------------------------")
print("Simulation complete. The lifts are waiting for the next passenger.")