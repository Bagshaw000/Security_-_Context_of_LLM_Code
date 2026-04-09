import random
import time

class Lift:
    def __init__(self, name, num_floors):
        self.name = name
        self.current_floor = 1
        self.num_floors = num_floors
        self.passengers = []

    def move_to_floor(self, floor):
        print(f"{self.name} moving from floor {self.current_floor} to floor {floor}")
        self.current_floor = floor

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        print(f"{passenger} has entered {self.name}")

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)
        print(f"{passenger} has exited {self.name}")

    def run(self):
        while True:
            destination_floor = random.randint(1, self.num_floors)
            if destination_floor != self.current_floor:
                self.move_to_floor(destination_floor)
                for passenger in self.passengers[:]:
                    if passenger.destination == self.current_floor:
                        self.remove_passenger(passenger)
                time.sleep(2)

class Passenger:
    def __init__(self, name, destination):
        self.name = name
        self.destination = destination

    def __str__(self):
        return self.name


lift1 = Lift("Lift 1", 50)
lift2 = Lift("Lift 2", 50)
lift3 = Lift("Lift 3", 50)


passenger1 = Passenger("John", 25)
passenger2 = Passenger("Jane", 15)
passenger3 = Passenger("Bob", 40)
passenger4 = Passenger("Alice", 10)


lift1.add_passenger(passenger1)
lift2.add_passenger(passenger2)
lift3.add_passenger(passenger3)
lift3.add_passenger(passenger4)


lift1.run()
lift2.run()
lift3.run()