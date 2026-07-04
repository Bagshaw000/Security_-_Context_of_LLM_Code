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

    def pick_up(self, floor):
        print(f"Lift {self.id} picking up passengers at floor {floor}.")
        self.move(floor)
        self.passengers.append(floor)

    def drop_off(self, floor):
        if floor in self.passengers:
            print(f"Lift {self.id} dropping off passengers at floor {floor}.")
            self.passengers.remove(floor)
            self.move(0)

class Building:
    def __init__(self, num_lifts):
        self.lifts = [Lift(i) for i in range(num_lifts)]

    def request_lift(self, floor):
        available_lift = random.choice(self.lifts)
        threading.Thread(target=available_lift.pick_up, args=(floor,)).start()

def main():
    building = Building(3)
    for _ in range(5):
        requested_floor = random.randint(0, 10)
        print(f"Requesting lift to floor {requested_floor}.")
        building.request_lift(requested_floor)
        time.sleep(2)

if __name__ == "__main__":
    main()