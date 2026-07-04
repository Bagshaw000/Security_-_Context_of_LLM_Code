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
        time.sleep(abs(target_floor - self.current_floor))  
        self.current_floor = target_floor
        print(f"Lift {self.id} arrived at floor {self.current_floor}")

    def call(self, floor):
        self.direction = 'up' if floor > self.current_floor else 'down'
        self.move(floor)

    def load_passengers(self, passengers):
        self.passengers.extend(passengers)
        print(f"Lift {self.id} loaded passengers: {passengers}")

    def unload_passengers(self):
        print(f"Lift {self.id} unloading passengers: {self.passengers}")
        self.passengers.clear()

class Building:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(i) for i in range(num_lifts)]

    def request_lift(self, floor):
        lift = random.choice(self.lifts)
        lift.call(floor)

    def simulate(self):
        while True:
            floor = random.randint(0, self.num_floors - 1)
            self.request_lift(floor)
            time.sleep(random.randint(1, 3))

if __name__ == "__main__":
    building = Building(num_floors=10, num_lifts=3)
    threading.Thread(target=building.simulate).start()