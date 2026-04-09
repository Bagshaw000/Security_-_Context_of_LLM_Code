import time
import random



number_of_floors = 10
number_of_lifts = 3




lift_positions = [1, 1, 1]
lift_names = ["Lift A", "Lift B", "Lift C"]

print("--- SKYSCRAPER LIFT SIMULATION STARTING ---")
print(f"The building has {number_of_floors} floors and {number_of_lifts} lifts.")


for person_number in range(1, 6):
    print(f"\n--- Person 
    
    
    start_floor = random.randint(1, number_of_floors)
    destination_floor = random.randint(1, number_of_floors)
    
    
    while destination_floor == start_floor:
        destination_floor = random.randint(1, number_of_floors)

    print(f"A person on Floor {start_floor} presses the button to go to Floor {destination_floor}.")

    
    
    
    closest_lift_index = 0
    shortest_distance = abs(lift_positions[0] - start_floor)

    for i in range(1, number_of_lifts):
        distance_to_person = abs(lift_positions[i] - start_floor)
        if distance_to_person < shortest_distance:
            shortest_distance = distance_to_person
            closest_lift_index = i

    chosen_lift_name = lift_names[closest_lift_index]
    starting_location = lift_positions[closest_lift_index]

    print(f"{chosen_lift_name} is dispatched from Floor {starting_location}.")

    
    
    time.sleep(1)
    print(f"{chosen_lift_name} arrives at Floor {start_floor}. Doors opening...")
    lift_positions[closest_lift_index] = start_floor

    
    time.sleep(1)
    print(f"{chosen_lift_name} is moving to Floor {destination_floor}...")
    lift_positions[closest_lift_index] = destination_floor
    
    time.sleep(1)
    print(f"{chosen_lift_name} has arrived at Floor {destination_floor}. Doors opening. Have a nice day!")

    
    print("Current locations of all lifts:")
    for i in range(number_of_lifts):
        print(f"  {lift_names[i]}: Floor {lift_positions[i]}")

print("\n--- SIMULATION COMPLETE ---")
print("All passengers have reached their destinations.")