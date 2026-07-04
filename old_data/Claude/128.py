import random
import time

class Lift:
    def __init__(self, name, num_floors):
        self.name = name
        self.num_floors = num_floors
        self.current_floor = 1
        self.passengers = []

    def call_lift(self, floor):
        print(f"{self.name} has been called to floor {floor}.")
        self.move_to_floor(floor)

    def move_to_floor(self, floor):
        travel_time = abs(self.current_floor - floor) * 0.5
        print(f"{self.name} is moving from floor {self.current_floor} to floor {floor}.")
        time.sleep(travel_time)
        self.current_floor = floor
        print(f"{self.name} has arrived at floor {self.current_floor}.")

    def board_passenger(self, passenger):
        self.passengers.append(passenger)
        print(f"{passenger} has boarded {self.name}.")

    def unboard_passenger(self, passenger):
        self.passengers.remove(passenger)
        print(f"{passenger} has disembarked from {self.name}.")

class Skyscraper:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(f"Lift {i+1}", num_floors) for i in range(num_lifts)]

    def simulate_day(self):
        while True:
            for lift in self.lifts:
                for passenger in lift.passengers:
                    if passenger.destination == lift.current_floor:
                        lift.unboard_passenger(passenger)
                        print(f"{passenger} has reached their destination.")

            random_floor = random.randint(1, self.num_floors)
            random_lift = random.choice(self.lifts)
            random_lift.call_lift(random_floor)

            time.sleep(2)

class Passenger:
    def __init__(self, name, start_floor, destination_floor):
        self.name = name
        self.start_floor = start_floor
        self.destination_floor = destination_floor

    def __str__(self):
        return self.name

skyscraper = Skyscraper(50, 10)

passengers = [
    Passenger("Alice", 10, 35),
    Passenger("Bob", 5, 20),
    Passenger("Charlie", 30, 15),
    Passenger("David", 25, 40),
    Passenger("Eve", 45, 5)
]

for passenger in passengers:
    random_lift = random.choice(skyscraper.lifts)
    random_lift.board_passenger(passenger)

skyscraper.simulate_day()