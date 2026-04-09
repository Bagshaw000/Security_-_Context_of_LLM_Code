import random
import time
import threading

class Lift:
    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.direction = None
        self.passengers = []

    def move(self, target_floor):
        print(f"Lift {self.id} moving from floor {self.current_floor} to {target_floor}")
        time.sleep(abs(self.current_floor - target_floor))  
        self.current_floor = target_floor
        print(f"Lift {self.id} arrived at floor {self.current_floor}")

    def call_lift(self, floor):
        self.move(floor)

    def load_passengers(self, passengers):
        self.passengers.extend(passengers)
        print(f"Lift {self.id} loaded passengers: {self.passengers}")

    def unload_passengers(self):
        print(f"Lift {self.id} unloading passengers: {self.passengers}")
        self.passengers.clear()

class Building:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(i) for i in range(num_lifts)]

    def request_lift(self, floor, passengers):
        lift = random.choice(self.lifts)
        lift.call_lift(floor)
        lift.load_passengers(passengers)
        target_floor = random.randint(0, self.num_floors - 1)
        lift.move(target_floor)
        lift.unload_passengers()

def simulate_building():
    building = Building(num_floors=10, num_lifts=3)
    for _ in range(5):
        floor = random.randint(0, building.num_floors - 1)
        passengers = [f"Passenger {i}" for i in range(random.randint(1, 5))]
        threading.Thread(target=building.request_lift, args=(floor, passengers)).start()
        time.sleep(1)

simulate_building()