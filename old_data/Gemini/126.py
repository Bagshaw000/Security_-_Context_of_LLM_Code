import random
from enum import Enum
from typing import List, Set, Dict, Optional

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class Elevator:
    
    def __init__(self, elevator_id: int, total_floors: int):
        self.elevator_id = elevator_id
        self.total_floors = total_floors
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.targets: Set[int] = set()
        
        self.is_moving = False

    def add_stop(self, floor: int):
        
        if 0 <= floor < self.total_floors:
            self.targets.add(floor)
            if self.direction == Direction.IDLE:
                self._update_initial_direction(floor)

    def _update_initial_direction(self, target_floor: int):
        if target_floor > self.current_floor:
            self.direction = Direction.UP
        elif target_floor < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE

    def step(self):
        
        if self.direction == Direction.IDLE:
            return

        self.is_moving = True
        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        if self.current_floor in self.targets:
            self._handle_arrival()

    def _handle_arrival(self):
        
        print(f"[Elevator {self.elevator_id}] Arrived at floor {self.current_floor}")
        self.targets.remove(self.current_floor)
        self.is_moving = False
        self._set_next_direction()

    def _set_next_direction(self):
        
        if not self.targets:
            self.direction = Direction.IDLE
            return

        if self.direction == Direction.UP:
            
            if not any(f > self.current_floor for f in self.targets):
                self.direction = Direction.DOWN if any(f < self.current_floor for f in self.targets) else Direction.IDLE
        elif self.direction == Direction.DOWN:
            
            if not any(f < self.current_floor for f in self.targets):
                self.direction = Direction.UP if any(f > self.current_floor for f in self.targets) else Direction.IDLE

    def __repr__(self):
        return f"Elevator(ID: {self.elevator_id}, Floor: {self.current_floor}, Dir: {self.direction.name}, Targets: {sorted(list(self.targets))})"

class Dispatcher:
    
    def __init__(self, num_elevators: int, num_floors: int):
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]
        self.num_floors = num_floors

    def request_elevator(self, floor: int, direction: Direction):
        
        best_elevator = self._find_optimal_elevator(floor, direction)
        print(f"[Dispatcher] Assigning floor {floor} to Elevator {best_elevator.elevator_id}")
        best_elevator.add_stop(floor)

    def _find_optimal_elevator(self, floor: int, direction: Direction) -> Elevator:
        
        best_elevator = None
        min_cost = float('inf')

        for elevator in self.elevators:
            cost = self._calculate_cost(elevator, floor, direction)
            if cost < min_cost:
                min_cost = cost
                best_elevator = elevator
        
        return best_elevator 

    def _calculate_cost(self, elevator: Elevator, target_floor: int, target_direction: Direction) -> float:
        distance = abs(elevator.current_floor - target_floor)

        
        if elevator.direction == Direction.IDLE:
            return float(distance)

        
        is_on_path = False
        if elevator.direction == Direction.UP and target_floor >= elevator.current_floor and target_direction == Direction.UP:
            is_on_path = True
        elif elevator.direction == Direction.DOWN and target_floor <= elevator.current_floor and target_direction == Direction.DOWN:
            is_on_path = True

        if is_on_path:
            return float(distance)

        
        
        return float(distance + (self.num_floors * 1.5))

    def update_system(self):
        
        for elevator in self.elevators:
            elevator.step()

def simulate_skyscraper():
    
    NUM_FLOORS = 30
    NUM_ELEVATORS = 3
    SIMULATION_STEPS = 40

    system = Dispatcher(NUM_ELEVATORS, NUM_FLOORS)

    
    system.request_elevator(15, Direction.UP)
    system.request_elevator(2, Direction.UP)
    system.request_elevator(28, Direction.DOWN)

    for step in range(SIMULATION_STEPS):
        print(f"\n--- Time Step {step} ---")
        system.update_system()
        
        for e in system.elevators:
            print(e)

        
        if step == 10:
            print("[Event] New request at Floor 10 going DOWN")
            system.request_elevator(10, Direction.DOWN)
        
        if step == 20:
            print("[Event] New request at Floor 25 going UP")
            system.request_elevator(25, Direction.UP)

if __name__ == "__main__":
    simulate_skyscraper()