import random
import time

class Lift:
    def __init__(self, name, floors):
        self.name = name
        self.current_floor = 0
        self.floors = floors
        self.passengers = []
        self.direction = "up"

    def call_lift(self, floor):
        print(f"{self.name} called to floor {floor}")
        self.passengers.append(floor)
        self.move()

    def move(self):
        while self.passengers:
            if self.direction == "up":
                if self.current_floor < max(self.passengers):
                    self.current_floor += 1
                    print(f"{self.name} moved to floor {self.current_floor}")
                    if self.current_floor in self.passengers:
                        self.passengers.remove(self.current_floor)
                        print(f"{self.name} stopped at floor {self.current_floor}")
                else:
                    self.direction = "down"
            else:
                if self.current_floor > min(self.passengers):
                    self.current_floor -= 1
                    print(f"{self.name} moved to floor {self.current_floor}")
                    if self.current_floor in self.passengers:
                        self.passengers.remove(self.current_floor)
                        print(f"{self.name} stopped at floor {self.current_floor}")
                else:
                    self.direction = "up"

class Skyscraper:
    def __init__(self, num_lifts, num_floors):
        self.lifts = [Lift(f"Lift {i+1}", num_floors) for i in range(num_lifts)]
        self.num_floors = num_floors

    def simulate(self):
        while True:
            floor = random.randint(0, self.num_floors-1)
            lift = random.choice(self.lifts)
            lift.call_lift(floor)
            time.sleep(1)

skyscraper = Skyscraper(3, 20)
skyscraper.simulate()