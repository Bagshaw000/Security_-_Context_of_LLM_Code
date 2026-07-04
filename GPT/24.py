class Lift:
    def __init__(self, id, current_floor=0):
        self.id = id
        self.current_floor = current_floor
        self.requests = []

    def move_to(self, floor):
        self.current_floor = floor
        print(f"Lift {self.id} moving to floor {floor}")

    def add_request(self, floor):
        self.requests.append(floor)
        print(f"Lift {self.id} received request for floor {floor}")

    def process_requests(self):
        while self.requests:
            next_floor = self.requests.pop(0)
            self.move_to(next_floor)


class Building:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.lifts = [Lift(i) for i in range(num_lifts)]

    def request_lift(self, floor):
        if floor < 0 or floor >= self.num_floors:
            print("Invalid floor request")
            return
        closest_lift = min(self.lifts, key=lambda lift: abs(lift.current_floor - floor))
        closest_lift.add_request(floor)
        closest_lift.process_requests()



if __name__ == "__main__":
    building = Building(num_floors=10, num_lifts=3)
    building.request_lift(5)
    building.request_lift(2)
    building.request_lift(8)