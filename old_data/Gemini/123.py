import random
import time
from enum import Enum
from typing import List, Set

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class Elevator:
    def __init__(self, elevator_id: int, total_floors: int):
        self.elevator_id = elevator_id
        self.current_floor = 0
        self.total_floors = total_floors
        self.targets: Set[int] = set()
        self.direction = Direction.IDLE

    def add_request(self, floor: int):
        if 0 <= floor < self.total_floors:
            self.targets.add(floor)
            self._update_direction()

    def _update_direction(self):
        if not self.targets:
            self.direction = Direction.IDLE
            return

        if self.direction == Direction.IDLE:
            if max(self.targets) > self.current_floor:
                self.direction = Direction.UP
            elif min(self.targets) < self.current_floor:
                self.direction = Direction.DOWN
        
    def step(self):
        
        if self.direction == Direction.IDLE:
            return

        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        if self.current_floor in self.targets:
            print(f"[Elevator {self.elevator_id}] Stopping at floor {self.current_floor}")
            self.targets.remove(self.current_floor)
            
            if not self.targets:
                self.direction = Direction.IDLE
            else:
                
                if self.direction == Direction.UP and all(t < self.current_floor for t in self.targets):
                    self.direction = Direction.DOWN
                elif self.direction == Direction.DOWN and all(t > self.current_floor for t in self.targets):
                    self.direction = Direction.UP

    def __repr__(self):
        return f"Elevator({self.elevator_id}) @ Floor {self.current_floor} | Dir: {self.direction.name} | Targets: {sorted(list(self.targets))}"

class Building:
    def __init__(self, num_floors: int, num_elevators: int):
        self.num_floors = num_floors
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]
        self.waiting_requests: List[int] = []

    def call_elevator(self, floor: int):
        print(f"[Building] Call registered from floor {floor}")
        
        best_elevator = None
        min_distance = self.num_floors + 1

        for elevator in self.elevators:
            distance = abs(elevator.current_floor - floor)
            
            
            if elevator.direction == Direction.IDLE:
                score = distance
            elif (elevator.direction == Direction.UP and floor >= elevator.current_floor) or \
                 (elevator.direction == Direction.DOWN and floor <= elevator.current_floor):
                score = distance
            else:
                score = distance + self.num_floors 

            if score < min_distance:
                min_distance = score
                best_elevator = elevator

        if best_elevator:
            best_elevator.add_request(floor)

    def run_simulation(self, steps: int = 20):
        for i in range(steps):
            print(f"\n--- Time Step {i} ---")
            
            
            if random.random() < 0.3:
                random_floor = random.randint(0, self.num_floors - 1)
                self.call_elevator(random_floor)

            for elevator in self.elevators:
                elevator.step()
                print(elevator)
            
            time.sleep(0.5)

def main():
    
    FLOORS = 10
    ELEVATORS = 3
    STEPS = 15

    skyscraper = Building(FLOORS, ELEVATORS)
    
    
    skyscraper.call_elevator(7)
    skyscraper.call_elevator(2)

    skyscraper.run_simulation(STEPS)

if __name__ == "__main__":
    main()