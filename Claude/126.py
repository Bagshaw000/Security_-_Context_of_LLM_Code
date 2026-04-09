import time
import random

class Lift:
    def __init__(self, name, num_floors):
        self.name = name
        self.current_floor = 1
        self.num_floors = num_floors
        self.passengers = []

    def move_up(self):
        if self.current_floor < self.num_floors:
            self.current_floor += 1
            print(f"{self.name} is moving up to floor {self.current_floor}")
        else:
            print(f"{self.name} is already on the top floor ({self.num_floors})")

    def move_down(self):
        if self.current_floor > 1:
            self.current_floor -= 1
            print(f"{self.name} is moving down to floor {self.current_floor}")
        else:
            print(f"{self.name} is already on the ground floor (1)")

    def add_passenger(self, passenger):
        self.passengers.append(passenger)
        print(f"{passenger} has entered {self.name}")

    def remove_passenger(self, passenger):
        self.passengers.remove(passenger)
        print(f"{passenger} has exited {self.name}")

def simulate_lifts(num_lifts, num_floors):
    lifts = []
    for i in range(1, num_lifts + 1):
        lift = Lift(f"Lift {i}", num_floors)
        lifts.append(lift)

    while True:
        for lift in lifts:
            if random.randint(1, 10) == 1:
                passenger = f"Passenger {random.randint(1, 100)}"
                lift.add_passenger(passenger)
            if random.randint(1, 10) == 1:
                if lift.passengers:
                    passenger = random.choice(lift.passengers)
                    lift.remove_passenger(passenger)
            if random.randint(1, 10) == 1:
                if random.randint(1, 2) == 1:
                    lift.move_up()
                else:
                    lift.move_down()
        time.sleep(1)

simulate_lifts(5, 50)