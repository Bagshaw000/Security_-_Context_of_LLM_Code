import enum
import time
from typing import List, Set, Optional

class Direction(enum.Enum):
    UP = 1
    DOWN = -1
    IDLE = 0

class Elevator:
    
    def __init__(self, elevator_id: int, top_floor: int):
        self.id = elevator_id
        self.current_floor = 0
        self.top_floor = top_floor
        self.direction = Direction.IDLE
        self.stops: Set[int] = set()
        self.door_open = False

    def add_stop(self, floor: int):
        if 0 <= floor <= self.top_floor:
            self.stops.add(floor)
            if self.direction == Direction.IDLE:
                if floor > self.current_floor:
                    self.direction = Direction.UP
                elif floor < self.current_floor:
                    self.direction = Direction.DOWN

    def step(self):
        
        if self.door_open:
            self.door_open = False
            return

        if self.direction == Direction.IDLE:
            return

        
        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

        
        if self.current_floor in self.stops:
            self.stops.remove(self.current_floor)
            self.door_open = True
            print(f"[Elevator {self.id}] Stopped at floor {self.current_floor}. Doors opening...")
            
            if not self.stops:
                self.direction = Direction.IDLE
            else:
                
                still_has_stops_ahead = any(
                    (self.direction == Direction.UP and s > self.current_floor) or
                    (self.direction == Direction.DOWN and s < self.current_floor)
                    for s in self.stops
                )
                if not still_has_stops_ahead:
                    self.direction = Direction.DOWN if self.direction == Direction.UP else Direction.UP

    def __repr__(self):
        status = "OPEN" if self.door_open else self.direction.name
        return f"Elevator(ID: {self.id}, Floor: {self.current_floor}, State: {status}, Stops: {sorted(list(self.stops))})"

class Dispatcher:
    
    @staticmethod
    def calculate_cost(elevator: Elevator, target_floor: int, target_direction: Direction) -> float:
        distance = abs(elevator.current_floor - target_floor)
        
        
        if elevator.direction == Direction.IDLE:
            return float(distance)
        
        moving_towards = (elevator.direction == Direction.UP and target_floor >= elevator.current_floor) or \
                         (elevator.direction == Direction.DOWN and target_floor <= elevator.current_floor)
        
        same_direction = (elevator.direction == target_direction)

        if moving_towards and same_direction:
            return float(distance)
        elif moving_towards and not same_direction:
            return distance + (elevator.top_floor * 0.5)
        else:
            
            return distance + (elevator.top_floor * 1.5)

class Skyscraper:
    def __init__(self, num_elevators: int, num_floors: int):
        self.num_floors = num_floors
        self.elevators = [Elevator(i, num_floors - 1) for i in range(num_elevators)]

    def call_elevator(self, floor: int, direction: Direction):
        print(f"[*] Call requested at floor {floor} to go {direction.name}")
        best_elevator = min(
            self.elevators,
            key=lambda e: Dispatcher.calculate_cost(e, floor, direction)
        )
        best_elevator.add_stop(floor)

    def run_simulation(self, ticks: int = 20):
        for i in range(ticks):
            print(f"\n--- Tick {i} ---")
            for e in self.elevators:
                e.step()
                print(e)
            time.sleep(0.1)

def main():
    
    tower = Skyscraper(num_elevators=3, num_floors=20)

    
    tower.call_elevator(5, Direction.UP)
    tower.call_elevator(18, Direction.DOWN)
    tower.call_elevator(2, Direction.UP)

    
    
    for tick in range(25):
        if tick == 5:
            
            tower.call_elevator(10, Direction.DOWN)
        
        if tick == 10:
            
            tower.elevators[0].add_stop(0)
            
        tower.run_simulation(1)

if __name__ == "__main__":
    main()