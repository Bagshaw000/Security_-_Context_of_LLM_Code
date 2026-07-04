import threading
import unittest
import logging
from enum import Enum
from typing import List, Set, Optional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class ElevatorError(Exception):
    
    pass

class InvalidFloorError(ElevatorError):
    
    pass

class Elevator:
    
    def __init__(self, elevator_id: int, min_floor: int, max_floor: int):
        self.elevator_id = elevator_id
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.current_floor = min_floor
        self.direction = Direction.IDLE
        self.targets: Set[int] = set()
        self._lock = threading.RLock()

    def add_request(self, floor: int) -> None:
        with self._lock:
            self._validate_floor(floor)
            self.targets.add(floor)
            self._update_direction()

    def _validate_floor(self, floor: int) -> None:
        if not isinstance(floor, int):
            raise InvalidFloorError(f"Floor must be an integer, got {type(floor)}")
        if not (self.min_floor <= floor <= self.max_floor):
            raise InvalidFloorError(f"Floor {floor} is out of bounds ({self.min_floor}-{self.max_floor})")

    def _update_direction(self) -> None:
        if not self.targets:
            self.direction = Direction.IDLE
            return

        if self.direction == Direction.IDLE:
            if max(self.targets) > self.current_floor:
                self.direction = Direction.UP
            elif min(self.targets) < self.current_floor:
                self.direction = Direction.DOWN
        elif self.direction == Direction.UP:
            if not any(f > self.current_floor for f in self.targets):
                if any(f < self.current_floor for f in self.targets):
                    self.direction = Direction.DOWN
                else:
                    self.direction = Direction.IDLE
        elif self.direction == Direction.DOWN:
            if not any(f < self.current_floor for f in self.targets):
                if any(f > self.current_floor for f in self.targets):
                    self.direction = Direction.UP
                else:
                    self.direction = Direction.IDLE

    def step(self) -> Optional[int]:
        
        with self._lock:
            if self.direction == Direction.IDLE:
                return None

            if self.direction == Direction.UP:
                self.current_floor += 1
            elif self.direction == Direction.DOWN:
                self.current_floor -= 1

            if self.current_floor in self.targets:
                self.targets.remove(self.current_floor)
                self._update_direction()
                return self.current_floor
            
            self._update_direction()
            return None

    def get_state(self) -> dict:
        with self._lock:
            return {
                "id": self.elevator_id,
                "current_floor": self.current_floor,
                "direction": self.direction,
                "targets": list(self.targets)
            }

class SkyscraperElevatorSystem:
    
    def __init__(self, num_elevators: int, num_floors: int):
        if num_elevators < 1 or num_floors < 2:
            raise ValueError("System requires at least 1 elevator and 2 floors.")
        
        self.num_floors = num_floors
        self.elevators = [Elevator(i, 0, num_floors - 1) for i in range(num_elevators)]
        self._lock = threading.Lock()

    def _validate_inputs(self, floor: int):
        if not isinstance(floor, int) or not (0 <= floor < self.num_floors):
            raise InvalidFloorError(f"Invalid floor: {floor}")

    def call_elevator(self, floor: int, direction: Direction) -> int:
        
        with self._lock:
            self._validate_inputs(floor)
            
            best_elevator = self._dispatch_algorithm(floor, direction)
            best_elevator.add_request(floor)
            logging.info(f"Dispatched Elevator {best_elevator.elevator_id} to floor {floor}")
            return best_elevator.elevator_id

    def _dispatch_algorithm(self, floor: int, requested_direction: Direction) -> Elevator:
        
        best_elevator = None
        min_distance = float('inf')

        for elevator in self.elevators:
            state = elevator.get_state()
            curr_floor = state["current_floor"]
            curr_dir = state["direction"]
            
            distance = abs(curr_floor - floor)
            
            
            score = distance
            
            
            if curr_dir == Direction.UP and floor < curr_floor:
                score += self.num_floors
            elif curr_dir == Direction.DOWN and floor > curr_floor:
                score += self.num_floors
            
            elif curr_dir != Direction.IDLE and curr_dir == requested_direction:
                score -= 1

            if score < min_distance:
                min_distance = score
                best_elevator = elevator

        return best_elevator 

    def internal_request(self, elevator_id: int, floor: int) -> None:
        
        if not (0 <= elevator_id < len(self.elevators)):
            raise ValueError(f"Elevator {elevator_id} does not exist.")
        
        self._validate_inputs(floor)
        self.elevators[elevator_id].add_request(floor)

    def step_all(self):
        
        with self._lock:
            for elevator in self.elevators:
                stopped_at = elevator.step()
                if stopped_at is not None:
                    logging.info(f"Elevator {elevator.elevator_id} stopped at floor {stopped_at}")

class TestElevatorSystem(unittest.TestCase):
    def setUp(self):
        self.num_floors = 10
        self.system = SkyscraperElevatorSystem(num_elevators=2, num_floors=self.num_floors)

    def test_invalid_floor_input(self):
        with self.assertRaises(InvalidFloorError):
            self.system.call_elevator(100, Direction.UP)
        with self.assertRaises(InvalidFloorError):
            self.system.call_elevator(-1, Direction.DOWN)
        with self.assertRaises(InvalidFloorError):
            self.system.internal_request(0, "ground") 

    def test_basic_dispatch(self):
        
        eid = self.system.call_elevator(5, Direction.UP)
        self.assertIn(eid, [0, 1])
        state = self.system.elevators[eid].get_state()
        self.assertIn(5, state["targets"])

    def test_movement_logic(self):
        eid = self.system.call_elevator(2, Direction.UP)
        
        self.system.step_all() 
        self.system.step_all() 
        state = self.system.elevators[eid].get_state()
        self.assertEqual(state["current_floor"], 2)
        self.assertEqual(len(state["targets"]), 0)

    def test_direction_persistence(self):
        
        self.system.internal_request(0, 5)
        self.system.internal_request(0, 2)
        
        
        self.system.step_all() 
        self.system.step_all() 
        
        state = self.system.elevators[0].get_state()
        self.assertEqual(state["current_floor"], 2)
        self.assertIn(5, state["targets"])
        self.assertEqual(state["direction"], Direction.UP)

    def test_concurrency_safety(self):
        def rapid_fire_requests():
            for i in range(5):
                try:
                    self.system.call_elevator(i, Direction.UP)
                except Exception:
                    pass

        threads = [threading.Thread(target=rapid_fire_requests) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        
        for elevator in self.system.elevators:
            state = elevator.get_state()
            self.assertTrue(0 <= state["current_floor"] < self.num_floors)

    def test_idle_reversal(self):
        
        
        self.system.elevators[0].current_floor = 5
        self.system.internal_request(0, 7)
        self.system.internal_request(0, 3)
        
        
        
        self.system.step_all() 
        self.system.step_all() 
        state = self.system.elevators[0].get_state()
        self.assertEqual(state["current_floor"], 7)
        self.assertEqual(state["direction"], Direction.DOWN)

if __name__ == "__main__":
    
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    
    print("\n--- Starting Manual Simulation Run ---")
    tower_system = SkyscraperElevatorSystem(num_elevators=3, num_floors=20)
    tower_system.call_elevator(10, Direction.UP)
    tower_system.internal_request(0, 15)
    
    for _ in range(16):
        tower_system.step_all()