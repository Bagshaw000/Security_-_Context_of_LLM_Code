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
        lift = min(self.lifts, key=lambda l: abs(l.current_floor - floor))
        lift.request(floor)

    def step(self):
        for lift in self.lifts:
            lift.move()

    def simulate(self, steps):
        for _ in range(steps):
            floor_request = random.randint(0, self.num_floors - 1)
            self.request_lift(floor_request)
            self.step()
            self.status()

    def status(self):
        for lift in self.lifts:
            print(f'Lift {lift.id}: Current Floor: {lift.current_floor}, Passengers: {list(lift.passengers)}')

if __name__ == "__main__":
    building = Building(num_floors=10, num_lifts=3)
    building.simulate(20)