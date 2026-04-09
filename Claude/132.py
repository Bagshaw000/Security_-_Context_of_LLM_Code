import random
import time

class Lift:
    def __init__(self, name, num_floors, wait_time):
        self.name = name
        self.num_floors = num_floors
        self.current_floor = 0
        self.wait_time = wait_time
        self.passengers = []

    def move_lift(self):
        if self.passengers:
            destination = self.passengers[0]
            if destination > self.current_floor:
                self.current_floor += 1
                print(f"{self.name} moved up to floor {self.current_floor}")
            elif destination < self.current_floor:
                self.current_floor -= 1
                print(f"{self.name} moved down to floor {self.current_floor}")
            else:
                print(f"{self.name} reached floor {self.current_floor}")
                self.passengers.pop(0)
        else:
            print(f"{self.name} is idle on floor {self.current_floor}")
        time.sleep(self.wait_time)

    def add_passenger(self, floor):
        self.passengers.append(floor)
        self.passengers.sort()
        print(f"{self.name} added a passenger going to floor {floor}")

class Skyscraper:
    def __init__(self, num_floors, num_lifts, wait_time):
        self.num_floors = num_floors
        self.lifts = []
        for i in range(num_lifts):
            lift = Lift(f"Lift {i+1}", num_floors, wait_time)
            self.lifts.append(lift)

    def simulate(self, num_passengers, max_floor):
        for _ in range(num_passengers):
            floor = random.randint(0, max_floor)
            lift = random.choice(self.lifts)
            lift.add_passenger(floor)
        while True:
            for lift in self.lifts:
                lift.move_lift()


skyscraper = Skyscraper(20, 4, 1)
skyscraper.simulate(50, 19)