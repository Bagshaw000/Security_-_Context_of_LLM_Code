import random

class Lift:
    def __init__(self, id):
        self.id = id
        self.is_operating = False
        self.floor_current = 1

    def start_lift(self):
        self.is_operating = True
        print(f"Lift {self.id} is starting to move.")

    def stop_lift(self):
        self.is_operating = False
        print(f"Lift {self.id} has stopped moving.")

class Skyscraper:
    def __init__(self, num_lifts):
        self.num_lifts = num_lifts
        self.lifts = [Lift(i+1) for i in range(num_lifts)]

    def simulate(self, start_floor, end_floor):
        print(f"Starting simulation from floor {start_floor} to floor {end_floor}.")
        for lift in self.lifts:
            if not lift.is_operating:
                continue
            while lift.floor_current < end_floor and lift.floor_current <= start_floor:
                move_amount = random.randint(1, 5)
                lift.floor_current += move_amount
                print(f"Lift {lift.id} is moving from floor {lift.floor_current}.")
        for lift in self.lifts:
            if not lift.is_operating:
                continue
            if lift.floor_current > end_floor:
                lift.stop_lift()


skyscraper = Skyscraper(5)


skyscraper.simulate(10, 20)