import enum
import logging
import uuid
from typing import List, Set, Dict, Optional


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ElevatorControlSystem")

class Direction(enum.Enum):
    
    UP = 1
    DOWN = -1
    IDLE = 0

class AccessControl:
    
    def __init__(self, restricted_floors: Set[int]):
        self._restricted_floors = restricted_floors

    def validate_access(self, floor: int, credentials: Dict[str, str]) -> bool:
        
        if floor in self._restricted_floors:
            
            is_authorized = credentials.get("role") == "ADMIN"
            if not is_authorized:
                logger.warning(f"Security Alert: Unauthorized access attempt to restricted floor {floor} by {credentials.get('user_id', 'Unknown')}")
            return is_authorized
        return True

class Elevator:
    
    def __init__(self, elevator_id: str, min_floor: int, max_floor: int):
        self.elevator_id = elevator_id
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.current_floor = min_floor
        self.direction = Direction.IDLE
        self.targets: Set[int] = set()

    def add_destination(self, floor: int):
        
        if not (self.min_floor <= floor <= self.max_floor):
            raise ValueError(f"Target floor {floor} out of range for {self.elevator_id}")
        
        self.targets.add(floor)
        self._update_direction()

    def _update_direction(self):
        
        if not self.targets:
            self.direction = Direction.IDLE
            return

        if self.direction == Direction.IDLE:
            
            target = next(iter(self.targets))
            if target > self.current_floor:
                self.direction = Direction.UP
            elif target < self.current_floor:
                self.direction = Direction.DOWN

    def move(self):
        
        if self.direction == Direction.IDLE:
            return

        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        logger.info(f"Elevator {self.elevator_id} at floor {self.current_floor}")

        if self.current_floor in self.targets:
            self._process_arrival()

    def _process_arrival(self):
        
        logger.info(f"Elevator {self.elevator_id} reached floor {self.current_floor}. Doors opening.")
        self.targets.discard(self.current_floor)
        
        
        if not self.targets:
            self.direction = Direction.IDLE
        else:
            has_higher = any(t > self.current_floor for t in self.targets)
            has_lower = any(t < self.current_floor for t in self.targets)
            
            if self.direction == Direction.UP and not has_higher:
                self.direction = Direction.DOWN if has_lower else Direction.IDLE
            elif self.direction == Direction.DOWN and not has_lower:
                self.direction = Direction.UP if has_higher else Direction.IDLE

class SkyscraperManager:
    
    def __init__(self, floor_count: int, elevator_count: int, secure_floors: Set[int]):
        if floor_count < 2 or elevator_count < 1:
            raise ValueError("Invalid building configuration: Minimum 2 floors and 1 elevator required.")
        
        self.floor_count = floor_count
        self.elevators = [
            Elevator(f"ELV-{uuid.uuid4().hex[:4].upper()}", 1, floor_count) 
            for _ in range(elevator_count)
        ]
        self.access_control = AccessControl(secure_floors)

    def request_floor(self, requested_floor: int, auth_context: Dict[str, str]):
        
        try:
            
            if not isinstance(requested_floor, int):
                raise TypeError("Floor request must be an integer.")

            if not (1 <= requested_floor <= self.floor_count):
                logger.error(f"Input Error: Floor {requested_floor} is outside building range.")
                return

            
            if not self.access_control.validate_access(requested_floor, auth_context):
                return

            
            target_lift = self._find_best_lift(requested_floor)
            target_lift.add_destination(requested_floor)
            logger.info(f"Dispatching {target_lift.elevator_id} to floor {requested_floor}")

        except Exception as e:
            
            logger.error(f"Internal System Error during dispatch: {str(e)}")

    def _find_best_lift(self, floor: int) -> Elevator:
        
        best_lift = self.elevators[0]
        min_score = float('inf')

        for lift in self.elevators:
            distance = abs(lift.current_floor - floor)
            
            
            if lift.direction == Direction.IDLE:
                score = distance
            elif (lift.direction == Direction.UP and floor >= lift.current_floor) or \
                 (lift.direction == Direction.DOWN and floor <= lift.current_floor):
                score = distance
            else:
                
                score = distance + (self.floor_count * 2)
            
            if score < min_score:
                min_score = score
                best_lift = lift
        
        return best_lift

    def step(self):
        
        for lift in self.elevators:
            lift.move()

def main():
    
    
    manager = SkyscraperManager(floor_count=50, elevator_count=3, secure_floors={50})

    
    requests = [
        (10, {"user_id": "u123", "role": "USER"}),
        (50, {"user_id": "u456", "role": "USER"}), 
        (50, {"user_id": "brad_admin", "role": "ADMIN"}), 
        (25, {"user_id": "u789", "role": "USER"})
    ]

    for floor, auth in requests:
        manager.request_floor(floor, auth)

    
    logger.info("Starting Simulation Ticks...")
    for i in range(30):
        manager.step()

if __name__ == "__main__":
    main()