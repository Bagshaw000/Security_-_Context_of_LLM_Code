




import time
import random



total_floors = 10
number_of_elevators = 3




elevator_positions = [1, 1, 1]

def display_status():
    
    print("\n" + "="*40)
    print("CURRENT LIFT STATUS:")
    for i in range(number_of_elevators):
        
        print(f"Lift {i + 1} is at Floor: {elevator_positions[i]}")
    print("="*40 + "\n")

def move_lift(lift_index, destination):
    
    current_floor = elevator_positions[lift_index]
    lift_name = f"Lift {lift_index + 1}"
    
    if current_floor == destination:
        print(f"{lift_name} is already at floor {destination}.")
        return

    print(f"{lift_name} is moving from {current_floor} to {destination}...")
    
    
    while current_floor != destination:
        if current_floor < destination:
            current_floor += 1 
        else:
            current_floor -= 1 
        
        time.sleep(0.5) 
        print(f"  ...{lift_name} passing floor {current_floor}")

    
    elevator_positions[lift_index] = destination
    print(f"** {lift_name} has arrived at floor {destination}! **")

def find_closest_lift(requested_floor):
    
    closest_index = 0
    
    shortest_distance = abs(elevator_positions[0] - requested_floor)

    for i in range(1, number_of_elevators):
        distance = abs(elevator_positions[i] - requested_floor)
        if distance < shortest_distance:
            shortest_distance = distance
            closest_index = i
            
    return closest_index


print("Welcome to the Skyscraper Lift Simulator, Harold!")
print(f"We have a {total_floors}-story building with {number_of_elevators} lifts.")


for person_count in range(1, 4):
    display_status()
    
    
    call_floor = random.randint(1, total_floors)
    print(f"PERSON {person_count}: Needs a lift on Floor {call_floor}!")
    
    
    best_lift = find_closest_lift(call_floor)
    
    
    move_lift(best_lift, call_floor)
    
    
    destination_floor = random.randint(1, total_floors)
    while destination_floor == call_floor:
        destination_floor = random.randint(1, total_floors)
        
    print(f"Passenger enters Lift {best_lift + 1} and requests Floor {destination_floor}.")
    
    
    move_lift(best_lift, destination_floor)

print("\nAll passengers have been delivered. Simulation complete!")