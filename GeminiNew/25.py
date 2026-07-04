import threading
import time
import logging
from enum import Enum, auto
from typing import List, Set, Optional
from queue import Queue, Empty


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(threadName)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger("SkyscraperLiftSystem")

class Direction(Enum):
    STATIONARY = auto()
    UP = auto()
    DOWN = auto()

class ElevatorConfig:
    
    MIN_FLOOR = 0
    MAX_FLOOR = 100
    CAPACITY = 15
    DOOR_OPEN_TIME = 1.0
    FLOOR_TRAVEL_TIME = 0.5

class SecurityException(Exception):
    
    pass

class Elevator:
    
    def __init__(self, elevator_id: int):
        self.elevator_id = elevator_id
        self.current_floor = ElevatorConfig.MIN_FLOOR
        self.direction = Direction.STATIONARY
        self.targets: Set[int] = set()
        self._lock = threading.Lock()
        self._is_active = True

    def add_target(self, floor: int) -> None:
        
        with self._lock:
            self.targets.add(floor)
            if self.direction == Direction.STATIONARY:
                self._update_direction()

    def _update_direction(self) -> None:
        
        if not self.targets:
            self.direction = Direction.STATIONARY
            return
        
        
        if any(f > self.current_floor for f in self.targets):
            self.direction = Direction.UP
        elif any(f < self.current_floor for f in self.targets):
            self.direction = Direction.DOWN

    def run_lifecycle(self) -> None:
        
        logger.info(f"Elevator-{self.elevator_id} lifecycle started.")
        while self._is_active:
            self._process_movement()
            time.sleep(0.1) 

    def _process_movement(self) -> None:
        with self._lock:
            if self.current_floor in self.targets:
                self._handle_arrival()
            
            if self.direction == Direction.STATIONARY:
                return

            
            time.sleep(ElevatorConfig.FLOOR_TRAVEL_TIME)
            
            if self.direction == Direction.UP:
                self.current_floor += 1
            elif self.direction == Direction.DOWN:
                self.current_floor -= 1
            
            logger.debug(f"Elevator-{self.elevator_id} at floor {self.current_floor}")

    def _handle_arrival(self) -> None:
        logger.info(f"Elevator-{self.elevator_id} STOPPED at floor {self.current_floor}")
        self.targets.remove(self.current_floor)
        
        time.sleep(ElevatorConfig.DOOR_OPEN_TIME)
        self._update_direction()

    def shutdown(self) -> None:
        self._is_active = False

class ElevatorController:
    
    def __init__(self, elevator_count: int):
        self.elevators = [Elevator(i) for i in range(elevator_count)]
        self.request_queue = Queue()
        self._threads: List[threading.Thread] = []
        self._running = False

    def start(self) -> None:
        
        self._running = True
        for e in self.elevators:
            t = threading.Thread(target=e.run_lifecycle, name=f"ElevatorThread-{e.elevator_id}", daemon=True)
            t.start()
            self._threads.append(t)
        
        dispatch_thread = threading.Thread(target=self._dispatch_loop, name="DispatcherThread", daemon=True)
        dispatch_thread.start()
        self._threads.append(dispatch_thread)
        logger.info(f"System started with {len(self.elevators)} units.")

    def submit_request(self, floor: int) -> None:
        
        try:
            self._validate_request(floor)
            self.request_queue.put(floor)
            logger.info(f"External request queued for floor: {floor}")
        except SecurityException as e:
            logger.warning(f"Rejected invalid request: {e}")

    def _validate_request(self, floor: int) -> None:
        
        if not isinstance(floor, int):
            raise SecurityException("Input must be an integer.")
        if floor < ElevatorConfig.MIN_FLOOR or floor > ElevatorConfig.MAX_FLOOR:
            raise SecurityException(f"Floor {floor} is outside building boundaries.")

    def _dispatch_loop(self) -> None:
        
        while self._running:
            try:
                target_floor = self.request_queue.get(timeout=1)
                optimal_lift = self._select_best_elevator(target_floor)
                optimal_lift.add_target(target_floor)
                self.request_queue.task_done()
            except Empty:
                continue

    def _select_best_elevator(self, target_floor: int) -> Elevator:
        
        best_lift = self.elevators[0]
        min_cost = float('inf')

        for lift in self.elevators:
            with lift._lock:
                distance = abs(lift.current_floor - target_floor)
                
                
                penalty = 0
                if lift.direction == Direction.UP and target_floor < lift.current_floor:
                    penalty = ElevatorConfig.MAX_FLOOR
                elif lift.direction == Direction.DOWN and target_floor > lift.current_floor:
                    penalty = ElevatorConfig.MAX_FLOOR
                
                cost = distance + penalty
                
                if cost < min_cost:
                    min_cost = cost
                    best_lift = lift
        
        return best_lift

class BuildingManagementSystem:
    
    def __init__(self):
        
        self.controller = ElevatorController(elevator_count=4)

    def initialize_system(self):
        self.controller.start()

    def simulate_traffic(self):
        
        requests = [10, 50, 2, 88, 15, 30, 0, 99]
        
        def mock_user_request(floor):
            self.controller.submit_request(floor)

        threads = []
        for r in requests:
            t = threading.Thread(target=mock_user_request, args=(r,))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()

if __name__ == "__main__":
    
    bms = BuildingManagementSystem()
    bms.initialize_system()
    
    logger.info("Starting High-Performance Lift Simulation...")
    bms.simulate_traffic()
    
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down Building Management System.")