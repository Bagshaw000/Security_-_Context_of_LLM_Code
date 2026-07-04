
import random
import time

class Lift:
    def __init__(self, name):
        self.name = name
        self.is_operational = True
        self.current_floor = 1

    def move_to(self, floor):
        if not self.is_operational:
            print(f"{self.name} is currently out of order.")
            return
        self.current_floor = floor
        print(f"{self.name} moved to floor {floor}.")

class Skyscraper:
    def __init__(self, num_lifts):
        self.num_lifts = num_lifts
        self.lifts = [Lift(f"Lift {i+1}") for i in range(num_lifts)]

    def simulate(self):
        for lift in self.lifts:
            if random.random() < 0.5: 
                floor_to_move_to = random.randint(2, len(self.lifts))
                lift.move_to(floor_to_move_to)
            else:
                print(f"{lift.name} is currently out of order.")
        time.sleep(random.uniform(1, 3)) 


skyscraper = Skyscraper(5)

while True:
    skyscraper.simulate()
