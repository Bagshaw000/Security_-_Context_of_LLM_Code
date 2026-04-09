class Lift:
    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.direction = None
        self.requests = []

    def move(self):
        if self.requests:
            target_floor = self.requests.pop(0)
            if target_floor > self.current_floor:
                self.direction = 'up'
                self.current_floor += 1
            elif target_floor < self.current_floor:
                self.direction = 'down'
                self.current_floor -= 1
            if self.current_floor == target_floor:
                self.direction = None

class Building:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(i) for i in range(num_lifts)]

    def request_lift(self, floor):
        closest_lift = min(self.lifts, key=lambda lift: abs(lift.current_floor - floor))
        closest_lift.requests.append(floor)

    def step(self):
        for lift in self.lifts:
            lift.move()

    def status(self):
        return [(lift.id, lift.current_floor, lift.direction) for lift in self.lifts]


building = Building(num_floors=10, num_lifts=3)
building.request_lift(5)
building.request_lift(2)

for _ in range(10):
    building.step()
    print(building.status())