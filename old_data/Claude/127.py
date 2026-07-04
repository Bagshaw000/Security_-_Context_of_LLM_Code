import random
import time

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
        print(f"{self.name} is now on floor {self.current_floor}")

    def board(self, passenger):
        self.passengers.append(passenger)
        print(f"{passenger} has boarded {self.name}")

    def disembark(self):
        for passenger in self.passengers:
            print(f"{passenger} has disembarked from {self.name}")
        self.passengers = []

def simulate_lifts(num_lifts, num_floors):
    lifts = []
    for i in range(num_lifts):
        lift = Lift(f"Lift {i+1}", num_floors)
        lifts.append(lift)

    while True:
        for lift in lifts:
            lift.move()
            if random.randint(1, 10) == 1:
                passenger = f"Passenger {random.randint(1, 100)}"
                lift.board(passenger)
            if lift.current_floor == 1 or lift.current_floor == lift.num_floors:
                lift.disembark()
        time.sleep(1)

simulate_lifts(3, 50)