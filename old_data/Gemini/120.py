import unittest
from enum import Enum

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"

class Elevator:
    
    def __init__(self, elevator_id, total_floors):
        self.id = elevator_id
        self.total_floors = total_floors
        self.current_floor = 0
        self.requests = set()
        self.direction = Direction.IDLE

    def add_request(self, floor):
        if 0 <= floor < self.total_floors:
            self.requests.add(floor)
            if self.direction == Direction.IDLE:
                self._update_initial_direction(floor)
            return True
        return False

    def _update_initial_direction(self, target_floor):
        if target_floor > self.current_floor:
            self.direction = Direction.UP
        elif target_floor < self.current_floor:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE

    def move(self):
        if self.direction == Direction.IDLE:
            return

        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        print(f"[Elevator {self.id}] Moved to floor {self.current_floor}")

        if self.current_floor in self.requests:
            self._handle_arrival()

    def _handle_arrival(self):
        print(f"[Elevator {self.id}] Stopping at floor {self.current_floor}. Doors opening...")
        self.requests.remove(self.current_floor)
        
        if not self.requests:
            self.direction = Direction.IDLE
        else:
            
            up_requests = any(f > self.current_floor for f in self.requests)
            down_requests = any(f < self.current_floor for f in self.requests)

            if self.direction == Direction.UP and not up_requests:
                self.direction = Direction.DOWN if down_requests else Direction.IDLE
            elif self.direction == Direction.DOWN and not down_requests:
                self.direction = Direction.UP if up_requests else Direction.IDLE

class Skyscraper:
    
    def __init__(self, num_floors, num_elevators):
        self.num_floors = num_floors
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]

    def handle_external_call(self, floor):
        
        if not (0 <= floor < self.num_floors):
            print(f"Floor {floor} is out of bounds.")
            return

        
        best_elevator = min(self.elevators, key=lambda e: abs(e.current_floor - floor))
        print(f"Dispatching Elevator {best_elevator.id} to floor {floor}")
        best_elevator.add_request(floor)

    def step(self):
        
        for elevator in self.elevators:
            elevator.move()

def run_demo():
    
    building = Skyscraper(num_floors=20, num_elevators=3)

    
    building.handle_external_call(5)
    building.handle_external_call(15)
    building.handle_external_call(2)

    
    for i in range(1, 11):
        print(f"\n--- Simulation Step {i} ---")
        building.step()
        
        
        if i == 4:
            print("New request received for floor 10!")
            building.handle_external_call(10)

class TestElevatorSystem(unittest.TestCase):
    def test_elevator_initial_state(self):
        elevator = Elevator(0, 10)
        self.assertEqual(elevator.current_floor, 0)
        self.assertEqual(elevator.direction, Direction.IDLE)

    def test_elevator_movement_up(self):
        elevator = Elevator(0, 10)
        elevator.add_request(2)
        elevator.move()
        self.assertEqual(elevator.current_floor, 1)
        self.assertEqual(elevator.direction, Direction.UP)
        elevator.move()
        self.assertEqual(elevator.current_floor, 2)
        self.assertEqual(elevator.direction, Direction.IDLE)

    def test_out_of_bounds_request(self):
        elevator = Elevator(0, 10)
        result = elevator.add_request(15)
        self.assertFalse(result)

if __name__ == "__main__":
    
    run_demo()
    
    
    print("\n" + "="*30)
    print("RUNNING UNIT TESTS")
    print("="*30)
    unittest.main(argv=[''], exit=False)