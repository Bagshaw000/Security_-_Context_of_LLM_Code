import time
import random

class Lift:
    def __init__(self, name, num_floors):
        self.name = name
        self.num_floors = num_floors
        self.current_floor = 1
        self.direction = 'up'
        self.passengers = []

    def move(self):
        if self.direction == 'up':
            self.current_floor += 1
            if self.current_floor > self.num_floors:
                self.direction = 'down'
        else:
            self.current_floor -= 1
            if self.current_floor < 1:
                self.direction = 'up'
        time.sleep(1)
        print(f"{self.name} is on floor {self.current_floor}")

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        print(f"{passenger} has entered {self.name}")

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)
        print(f"{passenger} has exited {self.name}")

def simulate_lifts(num_lifts, num_floors):
    lifts = [Lift(f"Lift {i}", num_floors) for i in range(1, num_lifts+1)]

    while True:
        for lift in lifts:
            lift.move()

            for passenger in lift.passengers[:]:
                if passenger.destination == lift.current_floor:
                    lift.remove_passenger(passenger)

            if random.random() < 0.1:
                passenger = f"Passenger {random.randint(1, 100)}"
                destination = random.randint(1, num_floors)
                lift.add_passenger(passenger)
                print(f"{passenger} wants to go to floor {destination}")

if __name__ == "__main__":
    simulate_lifts(3, 20)