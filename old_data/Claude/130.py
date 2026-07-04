import random
import time

class Lift:
    def __init__(self, name, floors):
        self.name = name
        self.floors = floors
        self.current_floor = 0
        self.passengers = []

    def call_lift(self, floor):
        self.passengers.append(floor)
        print(f"Lift {self.name} called to floor {floor}")

    def move_lift(self):
        while self.passengers:
            next_floor = self.passengers.pop(0)
            print(f"Lift {self.name} moving from floor {self.current_floor} to floor {next_floor}")
            self.current_floor = next_floor
            time.sleep(2)

class Building:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(f"Lift {i+1}", num_floors) for i in range(num_lifts)]

    def simulate(self, duration):
        for _ in range(duration):
            for lift in self.lifts:
                floor = random.randint(0, self.num_floors - 1)
                lift.call_lift(floor)
            for lift in self.lifts:
                lift.move_lift()
            time.sleep(1)


building = Building(20, 3)
building.simulate(10)