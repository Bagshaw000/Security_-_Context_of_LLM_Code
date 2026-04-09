import random
import time

class Lift:
    def __init__(self, name, num_floors):
        self.name = name
        self.current_floor = 0
        self.num_floors = num_floors
        self.passengers = []
        self.direction = "up"

    def move(self):
        if self.direction == "up":
            if self.current_floor < self.num_floors - 1:
                self.current_floor += 1
            else:
                self.direction = "down"
        else:
            if self.current_floor > 0:
                self.current_floor -= 1
            else:
                self.direction = "up"

    def add_passenger(self, passenger):
        self.passengers.append(passenger)

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)

class Skyscraper:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = []
        for i in range(num_lifts):
            self.lifts.append(Lift(f"Lift {i+1}", num_floors))

    def simulate(self, duration):
        for _ in range(duration):
            for lift in self.lifts:
                lift.move()
                for passenger in lift.passengers:
                    if passenger.destination == lift.current_floor:
                        lift.remove_passenger(passenger)
                        print(f"{passenger.name} has reached their destination on {lift.name}.")
                if random.randint(0, 10) < 3:
                    new_passenger = Passenger(f"Passenger {len(self.lifts)+len(self.lifts)*len(lift.passengers)}", random.randint(0, self.num_floors-1), random.randint(0, self.num_floors-1))
                    lift.add_passenger(new_passenger)
                    print(f"{new_passenger.name} has entered {lift.name}.")
            time.sleep(1)

class Passenger:
    def __init__(self, name, current_floor, destination):
        self.name = name
        self.current_floor = current_floor
        self.destination = destination


skyscraper = Skyscraper(20, 5)
skyscraper.simulate(60)