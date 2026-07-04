import time
import uuid
import hashlib
import json
import unittest
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Optional

class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class SecurityManager:
    @staticmethod
    def hash_access_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    @staticmethod
    def validate_request(user_id: str, floor: int, restricted_floors: List[int]) -> bool:
        if floor in restricted_floors:
            
            return False
        return True

class ICloudStorage(ABC):
    @abstractmethod
    def save_log(self, data: dict):
        pass

class MockAWSS3Storage(ICloudStorage):
    def __init__(self, bucket_name: str):
        self.bucket = bucket_name
        self.storage = {}

    def save_log(self, data: dict):
        log_id = str(uuid.uuid4())
        
        self.storage[log_id] = json.dumps(data)
        return log_id

class Lift:
    def __init__(self, lift_id: int, max_capacity: int, speed: float):
        self.lift_id = lift_id
        self.current_floor = 0
        self.target_floors = []
        self.direction = Direction.IDLE
        self.max_capacity = max_capacity
        self.current_load = 0
        self.speed = speed 
        self.door_open = False

    def add_request(self, floor: int):
        if floor not in self.target_floors:
            self.target_floors.append(floor)
            self.target_floors.sort()

    def move(self):
        if not self.target_floors:
            self.direction = Direction.IDLE
            return

        target = self.target_floors[0]
        if self.current_floor < target:
            self.direction = Direction.UP
            self.current_floor += 1
        elif self.current_floor > target:
            self.direction = Direction.DOWN
            self.current_floor -= 1

        if self.current_floor == target:
            self.target_floors.pop(0)
            self.open_doors()

    def open_doors(self):
        self.door_open = True
        self.door_open = False

    def update_load(self, passengers: int):
        if self.current_load + passengers <= self.max_capacity:
            self.current_load += passengers
            return True
        return False

class Skyscraper:
    def __init__(self, num_floors: int, num_lifts: int, storage: ICloudStorage):
        self.num_floors = num_floors
        self.storage = storage
        self.lifts = [Lift(i, max_capacity=10, speed=1.0) for i in range(num_lifts)]
        self.restricted_floors = [num_floors - 1] 

    def request_lift(self, floor: int, user_token: str):
        
        hashed_token = SecurityManager.hash_access_token(user_token)
        if not SecurityManager.validate_request(hashed_token, floor, self.restricted_floors):
            self.storage.save_log({"event": "UNAUTHORIZED_ACCESS", "floor": floor})
            return None

        
        best_lift = min(self.lifts, key=lambda l: abs(l.current_floor - floor))
        best_lift.add_request(floor)
        
        self.storage.save_log({
            "event": "LIFT_REQUESTED",
            "lift_id": best_lift.lift_id,
            "floor": floor
        })
        return best_lift.lift_id

    def check_collisions(self) -> bool:
        
        
        positions = [l.current_floor for l in self.lifts]
        
        
        return len(positions) == len(set(positions))

class TestLiftSystem(unittest.TestCase):
    def setUp(self):
        self.storage = MockAWSS3Storage("secure-lift-logs")
        self.building = Skyscraper(num_floors=50, num_lifts=3, storage=self.storage)

    def test_security_restriction(self):
        
        result = self.building.request_lift(49, "guest_token")
        self.assertIsNone(result)

    def test_lift_movement(self):
        lift = self.building.lifts[0]
        lift.add_request(5)
        lift.move()
        self.assertEqual(lift.current_floor, 1)
        self.assertEqual(lift.direction, Direction.UP)

    def test_capacity_limit(self):
        lift = self.building.lifts[0]
        success = lift.update_load(11) 
        self.assertFalse(success)

    def test_data_logging(self):
        self.building.request_lift(10, "valid_token")
        self.assertTrue(len(self.storage.storage) > 0)

    def test_collision_detection(self):
        
        self.building.lifts[0].current_floor = 10
        self.building.lifts[1].current_floor = 10
        
        has_no_collision = self.building.check_collisions()
        self.assertFalse(has_no_collision)

def run_simulation():
    
    storage = MockAWSS3Storage("skyscraper-s3")
    building = Skyscraper(num_floors=20, num_lifts=2, storage=storage)
    
    print("Starting Skyscraper Lift Simulation...")
    
    
    building.request_lift(5, "user_alpha_token")
    building.request_lift(12, "user_beta_token")
    
    
    for _ in range(5):
        for lift in building.lifts:
            lift.move()
            print(f"Lift {lift.lift_id} is at floor {lift.current_floor}")
        
        if not building.check_collisions():
            print("Safety Alert: Lifts proximity warning.")

if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLiftSystem)
    unittest.TextTestRunner(verbosity=1).run(suite)
    
    
    run_simulation()