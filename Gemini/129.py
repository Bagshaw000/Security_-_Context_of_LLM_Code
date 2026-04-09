import time
import random
from enum import Enum
from typing import List, Set, Dict

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class Elevator:
    
    def __init__(self, elevator_id: int, total_floors: int):
        self.id = elevator_id
        self.total_floors = total_floors
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.internal_requests: Set[int] = set()
        self.door_open = False

    def add_destination(self, floor: int):
        if 0 <= floor < self.total_floors:
            self.internal_requests.add(floor)
            if self.direction == Direction.IDLE:
                self._set_initial_direction(floor)

    def _set_initial_direction(self, target: int):
        if target > self.current_floor:
            self.direction = Direction.UP
        elif target < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE

    def step(self):
        
        if self.door_open:
            self.door_open = False
            return

        if self.direction == Direction.IDLE:
            return

        
        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        
        if self.current_floor in self.internal_requests:
            self.internal_requests.remove(self.current_floor)
            self.door_open = True
            self._update_direction()

    def _update_direction(self):
        if not self.internal_requests:
            self.direction = Direction.IDLE
            return

        
        if self.direction == Direction.UP:
            if not any(f > self.current_floor for f in self.internal_requests):
                self.direction = Direction.DOWN if any(f < self.current_floor for f in self.internal_requests) else Direction.IDLE
        elif self.direction == Direction.DOWN:
            if not any(f < self.current_floor for f in self.internal_requests):
                self.direction = Direction.UP if any(f > self.current_floor for f in self.internal_requests) else Direction.IDLE

    def calculate_cost(self, target_floor: int) -> int:
        
        distance = abs(self.current_floor - target_floor)
        
        if self.direction == Direction.IDLE:
            return distance
        
        moving_towards = (self.direction == Direction.UP and target_floor > self.current_floor) or \
                         (self.direction == Direction.DOWN and target_floor < self.current_floor)
        
        if moving_towards:
            return distance
        else:
            
            return distance + (self.total_floors // 2)

    def __repr__(self):
        status = "OPEN" if self.door_open else self.direction.name
        return f"[Lift {self.id} | Floor {self.current_floor} | {status} | Req: {sorted(list(self.internal_requests))}]"

class BuildingController:
    
    def __init__(self, num_elevators: int, num_floors: int):
        self.num_floors = num_floors
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]

    def call_elevator(self, floor: int):
        
        if not (0 <= floor < self.num_floors):
            return

        
        best_elevator = min(self.elevators, key=lambda e: e.calculate_cost(floor))
        best_elevator.add_destination(floor)

    def run_tick(self):
        for e in self.elevators:
            e.step()

    def status(self):
        for e in self.elevators:
            print(e)

def simulate():
    
    FLOORS = 15
    LIFTS = 3
    TICKS = 20
    
    controller = BuildingController(LIFTS, FLOORS)
    
    
    controller.call_elevator(12)
    controller.call_elevator(3)
    
    for i in range(TICKS):
        print(f"\n--- Simulation Tick {i} ---")
        
        
        if i % 4 == 0:
            start = random.randint(0, FLOORS - 1)
            dest = random.randint(0, FLOORS - 1)
            if start != dest:
                print(f"New Request: Floor {start} -> Floor {dest}")
                controller.call_elevator(start)
                
                
        
        controller.run_tick()
        controller.status()
        time.sleep(0.2)

if __name__ == "__main__":
    simulate()