import random
import time







number_of_floors = 10
number_of_lifts = 3



lifts = []
for i in range(number_of_lifts):
    
    new_lift = {
        "id": i + 1,
        "current_floor": 0,
        "target_floor": 0,
        "passenger_destination": None,
        "status": "idle"  
    }
    lifts.append(new_lift)


waiting_requests = []



print("Starting the Skyscraper Lift Simulation...")
print("------------------------------------------")

for second in range(1, 21):
    print(f"Time: {second} seconds")

    
    if random.random() < 0.3:
        start_floor = random.randint(0, number_of_floors)
        end_floor = random.randint(0, number_of_floors)
        
        
        if start_floor != end_floor:
            print(f"  [!] A person on Floor {start_floor} wants to go to Floor {end_floor}.")
            waiting_requests.append({"from": start_floor, "to": end_floor})

    
    for person in waiting_requests[:]: 
        for lift in lifts:
            if lift["status"] == "idle":
                lift["target_floor"] = person["from"]
                lift["passenger_destination"] = person["to"]
                lift["status"] = "going_to_pickup"
                waiting_requests.remove(person)
                print(f"  [+] Lift {lift['id']} is heading to Floor {person['from']} to pick someone up.")
                break 

    
    for lift in lifts:
        
        if lift["current_floor"] < lift["target_floor"]:
            lift["current_floor"] += 1
        
        elif lift["current_floor"] > lift["target_floor"]:
            lift["current_floor"] -= 1
        
        else:
            if lift["status"] == "going_to_pickup":
                
                print(f"  [*] Lift {lift['id']} picked up the passenger at Floor {lift['current_floor']}.")
                lift["target_floor"] = lift["passenger_destination"]
                lift["status"] = "carrying_passenger"
            elif lift["status"] == "carrying_passenger":
                
                print(f"  [ok] Lift {lift['id']} dropped off the passenger at Floor {lift['current_floor']}.")
                lift["status"] = "idle"
                lift["passenger_destination"] = None

    
    status_report = "  Lifts: "
    for lift in lifts:
        status_report += f"[Lift {lift['id']} @ Floor {lift['current_floor']}] "
    print(status_report)
    print("------------------------------------------")

    
    time.sleep(1)

print("Simulation finished.")