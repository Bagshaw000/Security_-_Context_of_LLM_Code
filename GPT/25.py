class Lift:
    def __init__(self, id, total_floors):
        self.id = id
        self.current_floor = 0
        self.direction = None
        self.total_floors = total_floors
        self.requests = []

    def request_floor(self, floor):
        if 0 <= floor < self.total_floors:
            self.requests.append(floor)
            self.requests = sorted(set(self.requests))
            self.update_direction()

    def update_direction(self):
        if not self.requests:
            self.direction = None
        elif self.current_floor < self.requests[0]:
            self.direction = 'up'
        elif self.current_floor > self.requests[-1]:
            self.direction = 'down'
        else:
            self.direction = 'stopped'

    def move(self):
        if self.direction == 'up' and self.current_floor < self.total_floors - 1:
            self.current_floor += 1
        elif self.direction == 'down' and self.current_floor > 0:
            self.current_floor -= 1

        if self.current_floor in self.requests:
            self.requests.remove(self.current_floor)
            self.update_direction()

class Building:
    def __init__(self, total_floors, num_lifts):
        self.total_floors = total_floors
        self.lifts = [Lift(i, total_floors) for i in range(num_lifts)]

    def request_lift(self, floor):
        closest_lift = min(self.lifts, key=lambda lift: abs(lift.current_floor - floor))
        closest_lift.request_floor(floor)

    def step(self):
        for lift in self.lifts:
            lift.move()


if __name__ == "__main__":
    building = Building(total_floors=10, num_lifts=3)
    building.request_lift(5)
    building.request_lift(2)

    for _ in range(10):
        building.step()
        for lift in building.lifts:
            print(f"Lift {lift.id} is on floor {lift.current_floor} moving {lift.direction}")