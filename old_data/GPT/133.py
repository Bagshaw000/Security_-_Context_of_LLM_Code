import random
import time
from collections import deque

class Lift:
    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.direction = None
        self.passengers = deque()

    def move(self):
        if self.passengers:
            target_floor = self.passengers[0]
            if self.current_floor < target_floor:
                self.current_floor += 1
                self.direction = 'up'
            elif self.current_floor > target_floor:
                self.current_floor -= 1
                self.direction = 'down'
            if self.current_floor == target_floor:
                self.passengers.popleft()

    def request(self, floor):
        if floor not in self.passengers:
            self.passengers.append(floor)

class Building:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(i) for i in range(num_lifts)]

    def request_lift(self, floor):
        lift = min(self.lifts, key=lambda l: abs(l.current_floor - floor))
        lift.request(floor)

    def step(self):
        for lift in self.lifts:
            lift.move()

def simulate_building(num_floors, num_lifts, steps):
    building = Building(num_floors, num_lifts)
    for _ in range(steps):
        requested_floor = random.randint(0, num_floors - 1)
        building.request_lift(requested_floor)
        building.step()
        print(f"Lift states: {[{'id': lift.id, 'current_floor': lift.current_floor, 'passengers': list(lift.passengers)} for lift in building.lifts]}")
        time.sleep(1)

simulate_building(10, 3, 20)