Here's a Python code to simulate multiple lifts operating in a skyscraper:

import random
import time

class Lift:
    def __init__(self, name, num_floors):
        self.name = name
        self.num_floors = num_floors
        self.current_floor = 1
        self.passengers = []
        self.direction = 'up'

    def move(self):
        if self.direction == 'up':
            self.current_floor += 1
            if self.current_floor == self.num_floors:
                self.direction = 'down'
        else:
            self.current_floor -= 1
            if self.current_floor == 1:
                self.direction = 'up'
        print(f"{self.name} is on floor {self.current_floor}")

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)

class Passenger:
    def __init__(self, name, start_floor, end_floor):
        self.name = name
        self.start_floor = start_floor
        self.end_floor = end_floor

class Building:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(f"Lift {i+1}", num_floors) for i in range(num_lifts)]
        self.passengers = []

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def simulate(self):
        while True:
            for lift in self.lifts:
                lift.move()
                for passenger in lift.passengers:
                    if passenger.end_floor == lift.current_floor:
                        print(f"{passenger.name} has reached their destination on floor {passenger.end_floor}")
                        lift.remove_passenger(passenger)
                if len(self.passengers) > 0:
                    closest_passenger = min(self.passengers, key=lambda p: abs(p.start_floor - lift.current_floor))
                    if closest_passenger.start_floor == lift.current_floor:
                        lift.add_passenger(closest_passenger)
                        self.passengers.remove(closest_passenger)
                        print(f"{closest_passenger.name} has boarded {lift.name}")
            time.sleep(1)


building = Building(20, 3)
passenger1 = Passenger("John", 5, 15)
passenger2 = Passenger("Jane", 3, 10)
passenger3 = Passenger("Bob", 12, 7)
building.add_passenger(passenger1)
building.add_passenger(passenger2)
building.add_passenger(passenger3)
building.simulate()