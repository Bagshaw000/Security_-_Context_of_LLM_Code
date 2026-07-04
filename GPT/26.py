class Lift:
    def __init__(self, id):
        self.id = id
        self.current_floor = 0
        self.requests = []

    def move_to(self, floor):
        self.current_floor = floor
        print(f"Lift {self.id} moving to floor {floor}")

    def add_request(self, floor):
        self.requests.append(floor)
        print(f"Lift {self.id} received request for floor {floor}")

    def service_requests(self):
        while self.requests:
            next_floor = self.requests.pop(0)
            self.move_to(next_floor)

class Building:
    def __init__(self, num_lifts):
        self.lifts = [Lift(i) for i in range(num_lifts)]

    def request_lift(self, floor):
        closest_lift = min(self.lifts, key=lambda lift: abs(lift.current_floor - floor))
        closest_lift.add_request(floor)
        closest_lift.service_requests()


building = Building(3)
building.request_lift(5)
building.request_lift(2)
building.request_lift(8)