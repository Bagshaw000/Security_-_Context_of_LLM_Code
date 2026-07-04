import random
import time

class Lift:
    def __init__(self, name, floors, capacity):
        self.name = name
        self.floors = floors
        self.capacity = capacity
        self.current_floor = 0
        self.passengers = []

    def move(self, destination_floor):
        print(f"{self.name} moving from floor {self.current_floor} to floor {destination_floor}")
        self.current_floor = destination_floor
        time.sleep(2)

    def pickup(self, passenger):
        if len(self.passengers) < self.capacity:
            self.passengers.append(passenger)
            print(f"{self.name} picked up passenger {passenger} on floor {self.current_floor}")
        else:
            print(f"{self.name} is full and cannot pick up passenger {passenger} on floor {self.current_floor}")

    def dropoff(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            print(f"{self.name} dropped off passenger {passenger} on floor {self.current_floor}")
        else:
            print(f"{passenger} is not in {self.name}")

class Skyscraper:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.num_lifts = num_lifts
        self.lifts = []
        for i in range(num_lifts):
            lift = Lift(f"Lift {i+1}", num_floors, 4)
            self.lifts.append(lift)

    def simulate(self):
        while True:
            for lift in self.lifts:
                destination_floor = random.randint(0, self.num_floors-1)
                if destination_floor != lift.current_floor:
                    lift.move(destination_floor)
                    for passenger in lift.passengers:
                        if passenger.destination_floor == lift.current_floor:
                            lift.dropoff(passenger)
                    while len(lift.passengers) < lift.capacity:
                        passenger = Passenger(random.randint(0, self.num_floors-1), random.randint(0, self.num_floors-1))
                        if passenger.origin_floor != passenger.destination_floor:
                            lift.pickup(passenger)
                        else:
                            break
            time.sleep(5)

class Passenger:
    def __init__(self, origin_floor, destination_floor):
        self.origin_floor = origin_floor
        self.destination_floor = destination_floor

if __name__ == "__main__":
    skyscraper = Skyscraper(20, 4)
    skyscraper.simulate()