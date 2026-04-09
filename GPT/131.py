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
                self.direction = None

    def request(self, floor):
        if floor not in self.passengers:
            self.passengers.append(floor)

class Building:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(i) for i in range(num_lifts)]

    def request_lift(self, floor):
        closest_lift = min(self.lifts, key=lambda lift: abs(lift.current_floor - floor))
        closest_lift.request(floor)

    def step(self):
        for lift in self.lifts:
            lift.move()

def simulate_building(num_floors, num_lifts, num_requests, steps):
    building = Building(num_floors, num_lifts)
    for _ in range(num_requests):
        floor_request = random.randint(0, num_floors - 1)
        building.request_lift(floor_request)

    for _ in range(steps):
        building.step()
        time.sleep(0.5)
        for lift in building.lifts:
            print(f'Lift {lift.id} is at floor {lift.current_floor} with direction {lift.direction} and passengers {list(lift.passengers)}')

simulate_building(num_floors=10, num_lifts=3, num_requests=5, steps=20)