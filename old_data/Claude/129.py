import random
import time

class Lift:
    def __init__(self, name, max_capacity, current_floor):
        self.name = name
        self.max_capacity = max_capacity
        self.current_floor = current_floor
        self.passengers = []

    def add_passenger(self, passenger):
        if len(self.passengers) < self.max_capacity:
            self.passengers.append(passenger)
            print(f"{passenger} has entered {self.name}.")
        else:
            print(f"{self.name} is at full capacity and cannot accept {passenger}.")

    def remove_passenger(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            print(f"{passenger} has exited {self.name}.")
        else:
            print(f"{passenger} is not in {self.name}.")

    def move_to_floor(self, floor):
        print(f"{self.name} is moving from floor {self.current_floor} to floor {floor}.")
        self.current_floor = floor
        time.sleep(2)

class SkyscraperSimulation:
    def __init__(self, num_floors, num_lifts, max_capacity):
        self.num_floors = num_floors
        self.num_lifts = num_lifts
        self.max_capacity = max_capacity
        self.lifts = [Lift(f"Lift {i+1}", self.max_capacity, 1) for i in range(self.num_lifts)]
        self.passengers = []

    def add_passenger(self, passenger, start_floor, end_floor):
        self.passengers.append((passenger, start_floor, end_floor))
        print(f"{passenger} is waiting to go from floor {start_floor} to floor {end_floor}.")

    def simulate_lifts(self):
        while self.passengers:
            for lift in self.lifts:
                if self.passengers:
                    passenger, start_floor, end_floor = self.passengers.pop(0)
                    if lift.current_floor == start_floor:
                        lift.add_passenger(passenger)
                        lift.move_to_floor(end_floor)
                        lift.remove_passenger(passenger)
                    else:
                        lift.move_to_floor(start_floor)
                        lift.add_passenger(passenger)
                        lift.move_to_floor(end_floor)
                        lift.remove_passenger(passenger)
                else:
                    break
            time.sleep(1)


simulation = SkyscraperSimulation(20, 4, 5)
simulation.add_passenger("Alice", 3, 15)
simulation.add_passenger("Bob", 10, 5)
simulation.add_passenger("Charlie", 7, 12)
simulation.add_passenger("David", 1, 19)
simulation.add_passenger("Eve", 18, 2)
simulation.simulate_lifts()