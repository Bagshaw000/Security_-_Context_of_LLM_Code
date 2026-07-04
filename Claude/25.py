class Lift:
    def __init__(self, num_floors, capacity):
        self.num_floors = num_floors
        self.capacity = capacity
        self.current_floor = 1
        self.passengers = []

    def call_lift(self, floor):
        if floor < 1 or floor > self.num_floors:
            return "Invalid floor"
        self.move_to_floor(floor)
        return f"Lift arrived at floor {self.current_floor}"

    def board_passengers(self, passengers):
        if len(passengers) > self.capacity:
            return "Lift capacity exceeded"
        self.passengers.extend(passengers)
        return f"Passengers boarded: {len(self.passengers)}"

    def disembark_passengers(self, floor):
        disembarking = [p for p in self.passengers if p.destination == floor]
        self.passengers = [p for p in self.passengers if p.destination != floor]
        return f"{len(disembarking)} passengers disembarked at floor {floor}"

    def move_to_floor(self, floor):
        self.current_floor = floor

class Skyscraper:
    def __init__(self, num_floors, num_lifts, capacity):
        self.num_floors = num_floors
        self.lifts = [Lift(num_floors, capacity) for _ in range(num_lifts)]

    def call_lift(self, floor, passengers):
        available_lifts = [lift for lift in self.lifts if len(lift.passengers) < lift.capacity]
        if not available_lifts:
            return "No available lifts"
        closest_lift = min(available_lifts, key=lambda x: abs(x.current_floor - floor))
        return closest_lift.board_passengers(passengers)

    def run_simulation(self, passenger_requests):
        for floor, passengers in passenger_requests.items():
            self.call_lift(floor, passengers)
            for lift in self.lifts:
                lift.disembark_passengers(floor)

class Passenger:
    def __init__(self, destination):
        self.destination = destination


skyscraper = Skyscraper(num_floors=50, num_lifts=5, capacity=10)
passenger_requests = {
    2: [Passenger(destination=10), Passenger(destination=15), Passenger(destination=20)],
    5: [Passenger(destination=15), Passenger(destination=30), Passenger(destination=40)],
    10: [Passenger(destination=25), Passenger(destination=35), Passenger(destination=45)],
}
skyscraper.run_simulation(passenger_requests)