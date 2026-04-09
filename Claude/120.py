import time
import random

class Lift:
    def __init__(self, name, num_floors):
        self.name = name
        self.current_floor = 0
        self.num_floors = num_floors
        self.passengers = []

    def call_lift(self, floor):
        self.current_floor = floor
        print(f"Lift {self.name} has been called to floor {self.current_floor}.")

    def load_passengers(self, passengers):
        self.passengers = passengers
        print(f"Lift {self.name} has loaded {len(self.passengers)} passengers.")

    def move_to_floor(self, floor):
        time.sleep(1)
        self.current_floor = floor
        print(f"Lift {self.name} is moving to floor {self.current_floor}.")

    def unload_passengers(self):
        unloaded = self.passengers.copy()
        self.passengers.clear()
        print(f"Lift {self.name} has unloaded {len(unloaded)} passengers.")
        return unloaded

class SkyscraperSimulator:
    def __init__(self, num_lifts, num_floors):
        self.lifts = [Lift(f"Lift {i+1}", num_floors) for i in range(num_lifts)]
        self.num_floors = num_floors

    def simulate_day(self):
        while True:
            for lift in self.lifts:
                floor = random.randint(0, self.num_floors - 1)
                passengers = [f"Passenger {i+1}" for i in range(random.randint(1, 5))]
                lift.call_lift(floor)
                lift.load_passengers(passengers)
                new_floor = random.randint(0, self.num_floors - 1)
                lift.move_to_floor(new_floor)
                unloaded = lift.unload_passengers()
                print(f"Lift {lift.name} unloaded {len(unloaded)} passengers.")
            time.sleep(5)


simulator = SkyscraperSimulator(3, 20)
simulator.simulate_day()