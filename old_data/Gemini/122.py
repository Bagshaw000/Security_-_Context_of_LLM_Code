import enum
import time
import random
from typing import List, Set

class Direction(enum.Enum):
    UP = 1
    DOWN = -1
    STATIONARY = 0

class Elevator:
    
    def __init__(self, elevator_id: int, total_floors: int):
        self.id = elevator_id
        self.total_floors = total_floors
        self.current_floor = 0
        self.direction = Direction.STATIONARY
        self.requests: Set[int] = set()

    def add_request(self, floor: int):
        
        if 0 <= floor < self.total_floors:
            self.requests.add(floor)
            if self.direction == Direction.STATIONARY:
                self._determine_initial_direction(floor)

    def _determine_initial_direction(self, target_floor: int):
        if target_floor > self.current_floor:
            self.direction = Direction.UP
        elif target_floor < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.STATIONARY

    def step(self):
        
        if self.direction == Direction.STATIONARY:
            return

        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        if self.current_floor in self.requests:
            self.requests.remove(self.current_floor)
            print(f"[Elevator {self.id}] Door opening at floor {self.current_floor}")
            self._update_direction()

    def _update_direction(self):
        
        if not self.requests:
            self.direction = Direction.STATIONARY
            return

        if self.direction == Direction.UP:
            
            if not any(f > self.current_floor for f in self.requests):
                self.direction = Direction.DOWN if any(f < self.current_floor for f in self.requests) else Direction.STATIONARY
        elif self.direction == Direction.DOWN:
            
            if not any(f < self.current_floor for f in self.requests):
                self.direction = Direction.UP if any(f > self.current_floor for f in self.requests) else Direction.STATIONARY

class Skyscraper:
    
    def __init__(self, num_floors: int, num_elevators: int):
        self.num_floors = num_floors
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]

    def handle_external_call(self, floor: int):
        
        
        
        best_elevator = min(self.elevators, key=lambda e: abs(e.current_floor - floor))
        print(f"[System] Request for floor {floor} assigned to Elevator {best_elevator.id}")
        best_elevator.add_request(floor)

    def run_simulation(self, ticks: int):
        
        for t in range(ticks):
            print(f"\n--- Simulation Tick {t} ---")
            for e in self.elevators:
                e.step()
                print(f" Elevator {e.id} | Floor: {e.current_floor} | State: {e.direction.name} | Queue: {sorted(list(e.requests))}")
            
            
            if t % 4 == 0:
                random_floor = random.randint(0, self.num_floors - 1)
                self.handle_external_call(random_floor)
            
            time.sleep(0.1)


def test_elevator_movement():
    test_elevator = Elevator(id=99, total_floors=10)
    test_elevator.add_request(5)
    
    
    for _ in range(5):
        test_elevator.step()
    
    assert test_elevator.current_floor == 5
    assert test_elevator.direction == Direction.STATIONARY
    print("Unit Test: test_elevator_movement PASSED")

if __name__ == "__main__":
    
    test_elevator_movement()
    
    
    london_tower = Skyscraper(num_floors=15, num_elevators=3)
    
    
    london_tower.handle_external_call(10)
    london_tower.handle_external_call(2)
    
    
    london_tower.run_simulation(20)