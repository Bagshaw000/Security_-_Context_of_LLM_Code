import time
import random

class Elevator:
    
    def __init__(self, elevator_id, total_floors):
        self.elevator_id = elevator_id
        self.total_floors = total_floors
        self.current_floor = 0
        self.targets = set()
        self.direction = 0  

    def add_request(self, floor):
        if 0 <= floor < self.total_floors:
            self.targets.add(floor)
            if self.direction == 0:
                self._update_direction()
            return True
        return False

    def _update_direction(self):
        if not self.targets:
            self.direction = 0
        elif any(f > self.current_floor for f in self.targets) and self.direction >= 0:
            self.direction = 1
        elif any(f < self.current_floor for f in self.targets) and self.direction <= 0:
            self.direction = -1
        else:
            
            if any(f > self.current_floor for f in self.targets):
                self.direction = 1
            elif any(f < self.current_floor for f in self.targets):
                self.direction = -1

    def move(self):
        if self.direction == 0 and not self.targets:
            return

        
        if self.current_floor in self.targets:
            print(f"[Elevator {self.elevator_id}] Arrived at floor {self.current_floor}. Opening doors.")
            self.targets.remove(self.current_floor)
            if not self.targets:
                self.direction = 0
            else:
                self._update_direction()
            return

        
        new_floor = self.current_floor + self.direction
        if 0 <= new_floor < self.total_floors:
            self.current_floor = new_floor
            print(f"[Elevator {self.elevator_id}] Moving to floor {self.current_floor}...")
        else:
            self.direction = 0

class Skyscraper:
    
    def __init__(self, name, num_elevators, num_floors):
        self.name = name
        self.floors = num_floors
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]

    def handle_external_call(self, floor):
        
        
        best_elevator = min(self.elevators, key=lambda e: abs(e.current_floor - floor))
        best_elevator.add_request(floor)
        print(f"[System] Floor {floor} call assigned to Elevator {best_elevator.elevator_id}")

    def run_simulation(self, ticks=20):
        print(f"Starting simulation for {self.name}...")
        for t in range(ticks):
            print(f"\n--- Tick {t} ---")
            for elevator in self.elevators:
                elevator.move()
            
            
            if t % 5 == 0:
                random_floor = random.randint(0, self.floors - 1)
                self.handle_external_call(random_floor)
            
            time.sleep(0.1)



def test_elevator_logic():
    test_elevator = Elevator(99, 10)
    test_elevator.add_request(5)
    assert test_elevator.direction == 1
    
    for _ in range(5):
        test_elevator.move()
    assert test_elevator.current_floor == 5
    print("Unit test: elevator_logic passed.")

if __name__ == "__main__":
    
    test_elevator_logic()

    
    
    skyscraper = Skyscraper("Bristol Innovation Centre", 3, 15)
    
    
    skyscraper.handle_external_call(10)
    skyscraper.handle_external_call(2)
    
    
    skyscraper.run_simulation(25)