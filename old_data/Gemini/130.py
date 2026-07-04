import time







NUMBER_OF_FLOORS = 20
NUMBER_OF_LIFTS = 3





lift_positions = [1, 1, 1]

def find_closest_lift(requested_floor):
    
    chosen_lift_index = 0
    
    shortest_gap = abs(lift_positions[0] - requested_floor)

    
    for i in range(1, len(lift_positions)):
        gap = abs(lift_positions[i] - requested_floor)
        if gap < shortest_gap:
            shortest_gap = gap
            chosen_lift_index = i
            
    return chosen_lift_index

def move_lift_animation(lift_id, start_floor, end_floor):
    
    if start_floor == end_floor:
        print(f"Lift {lift_id + 1} is already at floor {end_floor}.")
        return

    print(f"\nLift {lift_id + 1} is starting its journey...")
    
    
    step = 1 if end_floor > start_floor else -1
    
    
    current = start_floor
    while current != end_floor:
        current += step
        time.sleep(0.5) 
        print(f"  > Lift {lift_id + 1} passing floor {current}...")
        
    print(f"DING! Lift {lift_id + 1} arrived at floor {end_floor}.")
    
    lift_positions[lift_id] = end_floor




print("WELCOME TO THE SKYSCRAPER LIFT SYSTEM")
print(f"Building Height: {NUMBER_OF_FLOORS} floors")
print(f"Lifts Available: {NUMBER_OF_LIFTS}")
print("-" * 40)

while True:
    
    print("\nCURRENT LIFT STATUS:")
    for i in range(len(lift_positions)):
        print(f"Lift {i+1}: Floor {lift_positions[i]}")

    print("\n[Type 'Q' to turn off the power and quit]")
    call_input = input(f"Someone is calling a lift! Which floor are they on (1-{NUMBER_OF_FLOORS})? ")

    
    if call_input.upper() == 'Q':
        print("Shutting down system. Have a nice day, Harold!")
        break

    
    if call_input.isdigit():
        pickup_floor = int(call_input)
        
        if 1 <= pickup_floor <= NUMBER_OF_FLOORS:
            
            best_lift = find_closest_lift(pickup_floor)
            
            
            move_lift_animation(best_lift, lift_positions[best_lift], pickup_floor)
            
            
            dest_input = input(f"The doors are open. Which floor would you like to go to? ")
            
            if dest_input.isdigit():
                destination = int(dest_input)
                if 1 <= destination <= NUMBER_OF_FLOORS:
                    move_lift_animation(best_lift, lift_positions[best_lift], destination)
                else:
                    print("That floor doesn't exist in this building!")
            else:
                print("Invalid destination. The person got out.")
        else:
            print(f"Please enter a floor between 1 and {NUMBER_OF_FLOORS}.")
    else:
        print("Input not recognized. Please enter a floor number.")

    print("-" * 40)