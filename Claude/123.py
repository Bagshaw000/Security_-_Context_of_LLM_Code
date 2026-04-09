class Lift:
    def __init__(self, name, max_capacity, current_floor):
        self.name = name
        self.max_capacity = max_capacity
        self.current_floor = current_floor
        self.passengers = []

    def call_lift(self, floor):
        print(f"Lift {self.name} called to floor {floor}.")
        self.current_floor = floor

    def board_passenger(self, passenger):
        if len(self.passengers) < self.max_capacity:
            self.passengers.append(passenger)
            print(f"{passenger} boarded lift {self.name}.")
        else:
            print(f"Lift {self.name} is at full capacity. {passenger} cannot board.")

    def unboard_passengers(self, target_floor):
        for passenger in self.passengers[:]:
            if passenger.destination == target_floor:
                self.passengers.remove(passenger)
                print(f"{passenger} disembarked at floor {target_floor}.")

class Passenger:
    def __init__(self, name, destination):
        self.name = name
        self.destination = destination

    def __str__(self):
        return self.name

class SkyscraperSimulator:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(f"Lift {i+1}", 8, 1) for i in range(num_lifts)]
        self.passengers = [
            Passenger(f"Passenger {i+1}", random.randint(1, num_floors))
            for i in range(random.randint(10, 20))
        ]

    def run(self):
        while self.passengers:
            passenger = self.passengers.pop(0)
            closest_lift = min(self.lifts, key=lambda lift: abs(lift.current_floor - passenger.destination))
            closest_lift.call_lift(passenger.destination)
            closest_lift.board_passenger(passenger)
            closest_lift.unboard_passengers(passenger.destination)

import random

simulator = SkyscraperSimulator(20, 4)
simulator.run()