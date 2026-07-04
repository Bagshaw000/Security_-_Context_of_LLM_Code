import time
import unittest
from enum import Enum
from typing import List, Set, Optional

class Direction(Enum):
    UP = 1
    DOWN = -1
    STATIONARY = 0

class Elevator:
    def __init__(self, elevator_id: int, current_floor: int = 0):
        self.elevator_id = elevator_id
        self.current_floor = current_floor
        self.targets: Set[int] = set()
        self.direction = Direction.STATIONARY

    def add_request(self, floor: int):
        
        self.targets.add(floor)
        self._set_direction()

    def _set_direction(self):
        
        if not self.targets:
            self.direction = Direction.STATIONARY
        elif self.direction == Direction.STATIONARY:
            if next(iter(self.targets)) > self.current_floor:
                self.direction = Direction.UP
            else:
                self.direction = Direction.DOWN
        

    def move(self):
        
        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        if self.current_floor in self.targets:
            self.targets.remove(self.current_floor)
            print(f"[Elevator {self.elevator_id}] Stopped at floor {self.current_floor}. Remaining: {self.targets}")
            
            
            if not self.targets:
                self.direction = Direction.STATIONARY
            elif self.direction == Direction.UP and not any(f > self.current_floor for f in self.targets):
                self.direction = Direction.DOWN if any(f < self.current_floor for f in self.targets) else Direction.STATIONARY
            elif self.direction == Direction.DOWN and not any(f < self.current_floor for f in self.targets):
                self.direction = Direction.UP if any(f > self.current_floor for f in self.targets) else Direction.STATIONARY

    def __repr__(self):
        return f"Elevator({self.elevator_id}, Floor: {self.current_floor}, Dir: {self.direction.name})"

class Skyscraper:
    def __init__(self, name: str, num_floors: int, num_elevators: int):
        self.name = name
        self.num_floors = num_floors
        self.elevators = [Elevator(i, current_floor=0) for i in range(num_elevators)]

    def handle_external_request(self, floor: int):
        
        if not (0 <= floor < self.num_floors):
            print(f"Floor {floor} is out of bounds for {self.name}.")
            return

        
        
        best_elevator = min(
            self.elevators, 
            key=lambda e: abs(e.current_floor - floor) + (20 if e.direction != Direction.STATIONARY else 0)
        )
        best_elevator.add_request(floor)
        print(f"Dispatched Elevator {best_elevator.elevator_id} to floor {floor}")

    def step(self):
        
        for elevator in self.elevators:
            elevator.move()

    def status(self):
        for e in self.elevators:
            print(e)

def simulate():
    
    tower = Skyscraper("Bristol Tech Plaza", num_floors=20, num_elevators=3)
    
    
    tower.handle_external_request(5)
    tower.handle_external_request(18)
    tower.handle_external_request(2)

    
    for i in range(20):
        print(f"\n--- Tick {i} ---")
        tower.step()
        tower.status()
        
        
        if i == 5:
            tower.handle_external_request(10)

class TestElevatorSystem(unittest.TestCase):
    def test_elevator_movement(self):
        e = Elevator(id=1, current_floor=0)
        e.add_request(2)
        e.move()
        self.assertEqual(e.current_floor, 1)
        e.move()
        self.assertEqual(e.current_floor, 2)
        self.assertEqual(len(e.targets), 0)

    def test_skyscraper_dispatch(self):
        tower = Skyscraper("Test", 10, 1)
        tower.handle_external_request(5)
        self.assertIn(5, tower.elevators[0].targets)

if __name__ == "__main__":
    
    simulate()
    
    
    print("\n" + "="*20)
    print("Running Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestElevatorSystem)
    unittest.TextTestRunner(verbosity=1).run(suite)