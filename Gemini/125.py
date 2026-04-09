import asyncio
import enum
import logging
import random
from typing import List, Set, Optional


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ElevatorSystem")

class Direction(enum.Enum):
    UP = 1
    DOWN = -1
    STATIONARY = 0

class ElevatorState(enum.Enum):
    IDLE = "IDLE"
    MOVING = "MOVING"
    DOORS_OPENING = "DOORS_OPENING"
    DOORS_CLOSING = "DOORS_CLOSING"

class Elevator:
    
    def __init__(self, elevator_id: int, total_floors: int):
        self.elevator_id = elevator_id
        self.total_floors = total_floors
        self.current_floor = 0
        self.direction = Direction.STATIONARY
        self.state = ElevatorState.IDLE
        self.stops: Set[int] = set()
        self.lock = asyncio.Lock()

    async def add_stop(self, floor: int):
        async with self.lock:
            if 0 <= floor < self.total_floors:
                self.stops.add(floor)
                if self.direction == Direction.STATIONARY:
                    self.direction = Direction.UP if floor > self.current_floor else Direction.DOWN
                    if floor == self.current_floor:
                        self.direction = Direction.STATIONARY
                logger.info(f"Elevator {self.elevator_id} added stop at floor {floor}")

    def _update_direction(self):
        if not self.stops:
            self.direction = Direction.STATIONARY
            return

        if self.direction == Direction.UP:
            if not any(f > self.current_floor for f in self.stops):
                if any(f < self.current_floor for f in self.stops):
                    self.direction = Direction.DOWN
                else:
                    self.direction = Direction.STATIONARY
        elif self.direction == Direction.DOWN:
            if not any(f < self.current_floor for f in self.stops):
                if any(f > self.current_floor for f in self.stops):
                    self.direction = Direction.UP
                else:
                    self.direction = Direction.STATIONARY

    async def run(self):
        while True:
            async with self.lock:
                if self.stops:
                    if self.current_floor in self.stops:
                        self.state = ElevatorState.DOORS_OPENING
                        logger.info(f"Elevator {self.elevator_id} OPENING DOORS at floor {self.current_floor}")
                        await asyncio.sleep(1) 
                        self.stops.remove(self.current_floor)
                        self.state = ElevatorState.DOORS_CLOSING
                        logger.info(f"Elevator {self.elevator_id} CLOSING DOORS at floor {self.current_floor}")
                        self._update_direction()
                    
                    if self.direction != Direction.STATIONARY:
                        self.state = ElevatorState.MOVING
                        self.current_floor += self.direction.value
                        logger.info(f"Elevator {self.elevator_id} moving to floor {self.current_floor}")
                else:
                    self.state = ElevatorState.IDLE
                    self.direction = Direction.STATIONARY

            await asyncio.sleep(1) 

class ElevatorController:
    
    def __init__(self, num_elevators: int, num_floors: int):
        self.num_floors = num_floors
        self.elevators = [Elevator(i, num_floors) for i in range(num_elevators)]

    def _calculate_cost(self, elevator: Elevator, target_floor: int) -> float:
        
        distance = abs(elevator.current_floor - target_floor)
        
        
        if elevator.direction == Direction.UP and target_floor < elevator.current_floor:
            return distance + self.num_floors
        if elevator.direction == Direction.DOWN and target_floor > elevator.current_floor:
            return distance + self.num_floors
        
        
        if elevator.state == ElevatorState.IDLE:
            return distance
            
        return distance + (len(elevator.stops) * 2)

    async def request_elevator(self, floor: int):
        logger.info(f"New request received for floor {floor}")
        best_elevator = min(self.elevators, key=lambda e: self._calculate_cost(e, floor))
        await best_elevator.add_stop(floor)

    async def start_system(self):
        tasks = [asyncio.create_task(e.run()) for e in self.elevators]
        await asyncio.gather(*tasks)

async def simulate_traffic(controller: ElevatorController):
    
    await asyncio.sleep(2)
    floors_to_request = [5, 2, 9, 1, 0, 7, 4]
    for f in floors_to_request:
        await controller.request_elevator(f)
        await asyncio.sleep(random.uniform(0.5, 2.0))

async def main():
    
    NUM_FLOORS = 15
    NUM_ELEVATORS = 3
    
    controller = ElevatorController(NUM_ELEVATORS, NUM_FLOORS)
    
    logger.info("Starting Amazon-scale Elevator Control System...")
    
    
    await asyncio.gather(
        controller.start_system(),
        simulate_traffic(controller)
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("System shutdown initiated.")