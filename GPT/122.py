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
        while self.current_floor != target_floor:
            if self.current_floor < target_floor:
                self.current_floor += 1
                self.direction = 'up'
            else:
                self.current_floor -= 1
                self.direction = 'down'
            print(f"Lift {self.id} is at floor {self.current_floor} moving {self.direction}.")
            time.sleep(1)

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

    def request_lift(self, target_floor, passengers):
        available_lift = random.choice(self.lifts)
        available_lift.load_passengers(passengers)
        available_lift.move(target_floor)
        available_lift.unload_passengers()

def simulate_building():
    building = Building(num_floors=10, num_lifts=3)
    for _ in range(5):
        target_floor = random.randint(0, building.num_floors - 1)
        passengers = [f'Passenger {i}' for i in range(random.randint(1, 5))]
        threading.Thread(target=building.request_lift, args=(target_floor, passengers)).start()
        time.sleep(2)

if __name__ == "__main__":
    simulate_building()