import time
import random




class Lift:
    def __init__(self, identity_number):
        
        self.identity_number = identity_number
        self.current_floor = 1
        self.destination_floor = 1
        self.door_status = "Closed"
        self.direction = "Stopped"

    def update_position(self):
        
        if self.current_floor < self.destination_floor:
            self.current_floor += 1
            self.direction = "Going Up"
            self.door_status = "Closed"
        
        elif self.current_floor > self.destination_floor:
            self.current_floor -= 1
            self.direction = "Going Down"
            self.door_status = "Closed"
        
        else:
            self.direction = "Stopped"
            self.door_status = "Open"

class Skyscraper:
    def __init__(self, name, number_of_floors, number_of_lifts):
        self.name = name
        self.total_floors = number_of_floors
        
        self.lifts = []
        for i in range(1, number_of_lifts + 1):
            self.lifts.append(Lift(i))

    def display_status(self):
        
        print(f"\n--- Current Status of {self.name} ---")
        for lift in self.lifts:
            print(f"Lift 
        print("---------------------------------------")

    def simulate(self, rounds_of_time):
        
        for i in range(rounds_of_time):
            print(f"\nTime Passing... (Tick {i + 1})")
            
            for lift in self.lifts:
                
                if lift.direction == "Stopped":
                    
                    if random.randint(1, 3) == 1: 
                        new_call = random.randint(1, self.total_floors)
                        lift.destination_floor = new_call
                        print(f"[!] Someone called Lift 
                
                
                lift.update_position()

            self.display_status()
            
            time.sleep(1)




my_building = Skyscraper("The Shard", 10, 3)



my_building.simulate(15)

print("\nSimulation complete. All passengers have reached their destinations.")