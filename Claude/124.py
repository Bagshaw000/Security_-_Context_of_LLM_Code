import random
import time

class Lift:
    def __init__(self, name, num_floors):
        self.name = name
        self.num_floors = num_floors
        self.current_floor = 1
        self.passengers = []
        self.direction = "up"

    def move(self):
        if self.direction == "up":
            if self.current_floor < self.num_floors:
                self.current_floor += 1
            else:
                self.direction = "down"
        else:
            if self.current_floor > 1:
                self.current_floor -= 1
            else:
                self.direction = "up"

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)

    def __str__(self):
        return f"{self.name} (Floor {self.current_floor})"

class Passenger:
    def __init__(self, start_floor, end_floor):
        self.start_floor = start_floor
        self.end_floor = end_floor

def simulate_lifts(num_lifts, num_floors, num_passengers):
    lifts = [Lift(f"Lift {i+1}", num_floors) for i in range(num_lifts)]
    passengers = [Passenger(random.randint(1, num_floors), random.randint(1, num_floors)) for _ in range(num_passengers)]

    while True:
        for lift in lifts:
            if lift.passengers:
                for passenger in lift.passengers[:]:
                    if passenger.end_floor == lift.current_floor:
                        lift.remove_passenger(passenger)
                        print(f"{passenger.start_floor} -> {passenger.end_floor} (Lift {lift.name})")
            lift.move()

        for passenger in passengers[:]:
            for lift in lifts:
                if lift.current_floor == passenger.start_floor and len(lift.passengers) < 5:
                    lift.add_passenger(passenger)
                    passengers.remove(passenger)
                    break

        time.sleep(1)

simulate_lifts(3, 20, 50)