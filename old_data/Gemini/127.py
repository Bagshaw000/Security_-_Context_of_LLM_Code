import time
from enum import Enum
from typing import List, Set, Optional

class Direction(Enum):
    STATIONARY = 0
    UP = 1
    DOWN = 2

class Elevator:
    
    def __init__(self, elevator_id: int, total_floors: int):
        self.elevator_id = elevator_id
        self.total_floors = total_floors
        self.current_floor = 0
        self.direction = Direction.STATIONARY
        self.requests: Set[int] = set()

    def add_request(self, floor: int) -> None:
        if 0 <= floor < self.total_floors:
            self.requests.add(floor)
            if self.direction == Direction.STATIONARY:
                self._update_direction()

    def _update_direction(self) -> None:
        if not self.requests:
            self.direction = Direction.STATIONARY
            return

        if self.direction == Direction.UP:
            if not any(f > self.current_floor for f in self.requests):
                self.direction = Direction.DOWN if any(f < self.current_floor for f in self.requests) else Direction.STATIONARY
        elif self.direction == Direction.DOWN:
            if not any(f < self.current_floor for f in self.requests):
                self.direction = Direction.UP if any(f > self.current_floor for f in self.requests) else Direction.STATIONARY
        else: 
            target = next(iter(self.requests))
            if target > self.current_floor:
                self.direction = Direction.UP
            elif target < self.current_floor:
                self.direction = Direction.DOWN

    def move(self) -> None:
        if self.direction == Direction.STATIONARY:
            return

        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        if self.current_floor in self.requests:
            self._handle_arrival()

    def _handle_arrival(self) -> None:
        print(f"[Elevator {self.elevator_id}] Arrived at floor {self.current_floor}. Doors opening...")
        self.requests.remove(self.current_floor)
        self._update_direction()

    def __repr__(self) -> str:
        return f"Elevator(ID: {self.elevator_id}, Floor: {self.current_floor}, Dir: {self.direction.name}, Tasks: {sorted(list(self.requests))})"

class Dispatcher:
    
    @staticmethod
    def find_best_elevator(elevators: List[Elevator], request_floor: int) -> Elevator:
        best_elevator = elevators[0]
        min_cost = float('inf')

        for elevator in elevators:
            cost = Dispatcher._calculate_cost(elevator, request_floor)
            if cost < min_cost:
                min_cost = cost
                best_elevator = elevator
        
        return best_elevator

    @staticmethod
    def _calculate_cost(elevator: Elevator, target_floor: int) -> float:
        distance = abs(elevator.current_floor - target_floor)
        
        
        if elevator.direction == Direction.STATIONARY:
            return float(distance)

        
        moving_towards = (elevator.direction == Direction.UP and target_floor >= elevator.current_floor) or \
                         (elevator.direction == Direction.DOWN and target_floor <= elevator.current_floor)

        if moving_towards:
            return float(distance)
        
        
        return float(distance + (elevator.total_floors * 2))

class Skyscraper:
    
    def __init__(self, floors: int, num_elevators: int):
        self.floors = floors
        self.elevators = [Elevator(i, floors) for i in range(num_elevators)]

    def call_elevator(self, floor: int) -> None:
        if not (0 <= floor < self.floors):
            print(f"Invalid floor request: {floor}")
            return
        
        target_elevator = Dispatcher.find_best_elevator(self.elevators, floor)
        print(f"Dispatcher: Assigned floor {floor} to Elevator {target_elevator.elevator_id}")
        target_elevator.add_request(floor)

    def step(self) -> None:
        
        for elevator in self.elevators:
            elevator.move()

    def status(self) -> None:
        for elevator in self.elevators:
            print(elevator)

def run_simulation():
    
    BUILDING_FLOORS = 20
    NUM_ELEVATORS = 3
    SIMULATION_STEPS = 15

    building = Skyscraper(BUILDING_FLOORS, NUM_ELEVATORS)

    
    building.call_elevator(10)
    building.call_elevator(2)
    building.call_elevator(18)

    for i in range(SIMULATION_STEPS):
        print(f"\n--- Time Step {i} ---")
        building.step()
        building.status()
        
        
        if i == 3:
            building.call_elevator(5)
        if i == 7:
            building.call_elevator(1)

if __name__ == "__main__":
    run_simulation()