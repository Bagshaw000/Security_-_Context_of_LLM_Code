import enum
from typing import List, Set, Optional

class Direction(enum.Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"

class Elevator:
    
    def __init__(self, elevator_id: int, top_floor: int):
        self.elevator_id = elevator_id
        self.top_floor = top_floor
        self.current_floor = 0
        self.targets: Set[int] = set()
        self.direction = Direction.IDLE

    def add_request(self, floor: int):
        if 0 <= floor <= self.top_floor:
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
            else:
                
                self.direction = Direction.IDLE

    def step(self):
        
        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        if self.current_floor in self.targets:
            self.targets.remove(self.current_floor)
            print(f"[Elevator {self.elevator_id}] Stopped at floor {self.current_floor}")
            
        
        if not self.targets:
            self.direction = Direction.IDLE
        else:
            
            if self.direction == Direction.UP:
                if not any(t > self.current_floor for t in self.targets):
                    self.direction = Direction.DOWN if any(t < self.current_floor for t in self.targets) else Direction.IDLE
            elif self.direction == Direction.DOWN:
                if not any(t < self.current_floor for t in self.targets):
                    self.direction = Direction.UP if any(t > self.current_floor for t in self.targets) else Direction.IDLE

    def __repr__(self):
        return f"Elevator(ID: {self.elevator_id}, Floor: {self.current_floor}, Dir: {self.direction.value}, Targets: {sorted(list(self.targets))})"

class Skyscraper:
    
    def __init__(self, num_elevators: int, num_floors: int):
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]
        self.num_floors = num_floors

    def request_elevator(self, floor: int):
        
        if not (0 <= floor <= self.num_floors):
            print(f"Floor {floor} is out of bounds.")
            return

        
        
        best_elevator = min(
            self.elevators, 
            key=lambda e: abs(e.current_floor - floor)
        )
        best_elevator.add_request(floor)
        print(f"Request at floor {floor} assigned to Elevator {best_elevator.elevator_id}")

    def run_simulation(self, steps: int):
        for i in range(steps):
            print(f"\n--- Simulation Step {i+1} ---")
            for elevator in self.elevators:
                elevator.step()
                print(elevator)


import unittest

class TestElevatorSystem(unittest.TestCase):
    def setUp(self):
        self.elevator = Elevator(id=1, top_floor=10)

    def test_initialization(self):
        self.assertEqual(self.elevator.current_floor, 0)
        self.assertEqual(self.elevator.direction, Direction.IDLE)

    def test_movement_up(self):
        self.elevator.add_request(2)
        self.assertEqual(self.elevator.direction, Direction.UP)
        self.elevator.step()
        self.assertEqual(self.elevator.current_floor, 1)
        self.elevator.step()
        self.assertEqual(self.elevator.current_floor, 2)
        self.assertEqual(self.elevator.direction, Direction.IDLE)

    def test_out_of_bounds_request(self):
        skyscraper = Skyscraper(num_elevators=1, num_floors=10)
        skyscraper.request_elevator(15)
        self.assertEqual(len(skyscraper.elevators[0].targets), 0)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestElevatorSystem)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    
    building = Skyscraper(num_elevators=3, num_floors=20)
    
    
    building.request_elevator(5)
    building.request_elevator(18)
    building.request_elevator(2)
    
    
    building.run_simulation(10)

    
    print("\n[User interaction] Someone on floor 10 needs a lift...")
    building.request_elevator(10)
    building.run_simulation(10)

    print("\nStarting Unit Tests...")
    run_tests()