import time
import random
from enum import Enum
from typing import List, Set, Dict, Optional

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"

class Elevator:
    
    def __init__(self, elevator_id: int, current_floor: int = 0):
        self.elevator_id = elevator_id
        self.current_floor = current_floor
        self.direction = Direction.IDLE
        self.internal_requests: Set[int] = set()
        self.external_requests: Set[int] = set()
        self.capacity = 15
        self.load = 0

    def add_destination(self, floor: int):
        
        self.internal_requests.add(floor)
        self._set_initial_direction(floor)

    def add_external_request(self, floor: int):
        
        self.external_requests.add(floor)
        self._set_initial_direction(floor)

    def _set_initial_direction(self, target_floor: int):
        if self.direction == Direction.IDLE:
            if target_floor > self.current_floor:
                self.direction = Direction.UP
            elif target_floor < self.current_floor:
                self.direction = Direction.DOWN

    def move(self):
        
        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        self._process_floor_arrival()
        self._update_direction()

    def _process_floor_arrival(self):
        if self.current_floor in self.internal_requests or self.current_floor in self.external_requests:
            self.internal_requests.discard(self.current_floor)
            self.external_requests.discard(self.current_floor)
            print(f"[Elevator {self.elevator_id}] Door Open at Floor {self.current_floor}")

    def _update_direction(self):
        all_reqs = self.internal_requests.union(self.external_requests)
        if not all_reqs:
            self.direction = Direction.IDLE
            return

        if self.direction == Direction.UP:
            
            if not any(f > self.current_floor for f in all_reqs):
                self.direction = Direction.DOWN if any(f < self.current_floor for f in all_reqs) else Direction.IDLE
        elif self.direction == Direction.DOWN:
            
            if not any(f < self.current_floor for f in all_reqs):
                self.direction = Direction.UP if any(f > self.current_floor for f in all_reqs) else Direction.IDLE

    def get_status(self) -> str:
        return f"ID: {self.elevator_id} | Floor: {self.current_floor} | Dir: {self.direction.value} | Targets: {self.internal_requests.union(self.external_requests)}"

class Dispatcher:
    
    def __init__(self, elevators: List[Elevator]):
        self.elevators = elevators

    def assign_request(self, floor: int, direction: Direction):
        best_elevator = None
        min_cost = float('inf')

        for elevator in self.elevators:
            cost = self._calculate_cost(elevator, floor, direction)
            if cost < min_cost:
                min_cost = cost
                best_elevator = elevator
        
        if best_elevator:
            best_elevator.add_external_request(floor)
            print(f"[Dispatcher] Assigned floor {floor} ({direction.value}) to Elevator {best_elevator.elevator_id}")

    def _calculate_cost(self, elevator: Elevator, floor: int, req_direction: Direction) -> float:
        distance = abs(elevator.current_floor - floor)
        
        if elevator.direction == Direction.IDLE:
            return distance

        
        moving_towards = (elevator.direction == Direction.UP and floor >= elevator.current_floor) or \
                         (elevator.direction == Direction.DOWN and floor <= elevator.current_floor)
        
        
        same_direction = (elevator.direction == req_direction)

        if moving_towards and same_direction:
            return distance
        elif moving_towards and not same_direction:
            return distance + 15 
        else:
            return distance + 30 

class Skyscraper:
    def __init__(self, num_floors: int, num_elevators: int):
        self.num_floors = num_floors
        self.elevators = [Elevator(i, current_floor=random.randint(0, num_floors-1)) for i in range(num_elevators)]
        self.dispatcher = Dispatcher(self.elevators)

    def handle_external_call(self, floor: int, direction: Direction):
        print(f"[System] External call at floor {floor} going {direction.value}")
        self.dispatcher.assign_request(floor, direction)

    def step(self):
        for elevator in self.elevators:
            elevator.move()

    def display_state(self):
        for e in self.elevators:
            print(e.get_status())

def simulate():
    
    building = Skyscraper(num_floors=40, num_elevators=4)
    
    
    building.handle_external_call(10, Direction.UP)
    building.handle_external_call(35, Direction.DOWN)
    building.handle_external_call(2, Direction.UP)
    
    
    building.elevators[0].add_destination(20)

    
    for i in range(25):
        print(f"\n--- Tick {i} ---")
        building.step()
        building.display_state()
        
        
        if i == 5:
            building.handle_external_call(15, Direction.DOWN)
        if i == 10:
            building.handle_external_call(0, Direction.UP)
            
        time.sleep(0.1) 

if __name__ == "__main__":
    simulate()