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
        if self.direction == 'up':
            self.current_floor += 1
        elif self.direction == 'down':
            self.current_floor -= 1

    def set_direction(self, direction):
        self.direction = direction

    def add_passenger(self, floor):
        self.passengers.append(floor)

    def drop_passenger(self):
        if self.passengers and self.passengers[0] == self.current_floor:
            self.passengers.popleft()

class Building:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(i) for i in range(num_lifts)]
        self.requests = deque()

    def request_lift(self, floor):
        self.requests.append(floor)

    def step(self):
        for lift in self.lifts:
            lift.drop_passenger()
            if lift.passengers:
                lift.set_direction('up' if lift.current_floor < lift.passengers[0] else 'down')
            else:
                if self.requests:
                    lift.add_passenger(self.requests.popleft())
                    lift.set_direction('up' if lift.current_floor < lift.passengers[0] else 'down')
                else:
                    lift.set_direction(None)

            if lift.direction:
                lift.move()

    def simulate(self, steps):
        for _ in range(steps):
            self.step()
            time.sleep(1)
            self.status()

    def status(self):
        for lift in self.lifts:
            print(f'Lift {lift.id}: Floor {lift.current_floor}, Passengers: {list(lift.passengers)}')


building = Building(num_floors=10, num_lifts=3)
building.request_lift(5)
building.request_lift(2)
building.simulate(20)