import random
import time
from collections import deque

class Lift:
    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.direction = None
        self.requests = deque()

    def move(self):
        if self.requests:
            target_floor = self.requests.popleft()
            if self.current_floor < target_floor:
                self.direction = 'up'
                self.current_floor += 1
            elif self.current_floor > target_floor:
                self.direction = 'down'
                self.current_floor -= 1
            print(f"Lift {self.id} moving {self.direction} to floor {self.current_floor}")

    def request_floor(self, floor):
        if floor not in self.requests:
            self.requests.append(floor)
            print(f"Lift {self.id} received request for floor {floor}")

class Building:
    def __init__(self, num_lifts, num_floors):
        self.lifts = [Lift(i) for i in range(num_lifts)]
        self.num_floors = num_floors

    def request_lift(self, floor):
        closest_lift = min(self.lifts, key=lambda lift: abs(lift.current_floor - floor))
        closest_lift.request_floor(floor)

    def step(self):
        for lift in self.lifts:
            lift.move()

def simulate_building(num_lifts, num_floors, steps):
    building = Building(num_lifts, num_floors)
    for _ in range(steps):
        floor_request = random.randint(0, num_floors - 1)
        building.request_lift(floor_request)
        building.step()
        time.sleep(1)

simulate_building(num_lifts=3, num_floors=10, steps=20)