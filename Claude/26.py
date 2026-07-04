Here's a simple Python code to simulate multiple lifts operating in a skyscraper:

import random
import time

class Lift:
    def __init__(self, name, num_floors):
        self.name = name
        self.num_floors = num_floors
        self.current_floor = 1
        self.passengers = []

    def move_to_floor(self, floor):
        print(f"{self.name} is moving from floor {self.current_floor} to floor {floor}.")
        self.current_floor = floor

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        print(f"{passenger} has entered {self.name}.")

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)
        print(f"{passenger} has exited {self.name}.")

def simulate_lifts(num_lifts, num_floors, num_passengers):
    lifts = []
    passengers = [f"Passenger {i+1}" for i in range(num_passengers)]

    for i in range(num_lifts):
        lift = Lift(f"Lift {i+1}", num_floors)
        lifts.append(lift)

    while True:
        for lift in lifts:
            for passenger in passengers:
                if random.random() < 0.1:
                    lift.add_passenger(passenger)
                    target_floor = random.randint(1, lift.num_floors)
                    if target_floor != lift.current_floor:
                        lift.move_to_floor(target_floor)
                    lift.remove_passenger(passenger)
        time.sleep(1)


simulate_lifts(3, 20, 50)