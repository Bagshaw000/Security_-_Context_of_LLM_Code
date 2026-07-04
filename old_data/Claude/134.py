class Lift:
    def __init__(self, name, num_floors, capacity):
        self.name = name
        self.num_floors = num_floors
        self.capacity = capacity
        self.current_floor = 1
        self.passengers = []

    def call_lift(self, floor):
        if floor < 1 or floor > self.num_floors:
            print(f"Invalid floor {floor} for lift {self.name}")
            return
        print(f"Lift {self.name} called to floor {floor}")
        self.move_to_floor(floor)

    def move_to_floor(self, floor):
        print(f"Lift {self.name} moving from floor {self.current_floor} to floor {floor}")
        self.current_floor = floor

    def enter_lift(self, passenger):
        if len(self.passengers) >= self.capacity:
            print(f"Lift {self.name} is full, {passenger} cannot enter")
            return
        self.passengers.append(passenger)
        print(f"{passenger} entered lift {self.name}")

    def exit_lift(self, passenger):
        if passenger in self.passengers:
            self.passengers.remove(passenger)
            print(f"{passenger} exited lift {self.name}")
        else:
            print(f"{passenger} is not in lift {self.name}")

class SkyscraperSimulator:
    def __init__(self, num_floors, num_lifts):
        self.num_floors = num_floors
        self.num_lifts = num_lifts
        self.lifts = []
        for i in range(1, num_lifts + 1):
            self.lifts.append(Lift(f"Lift {i}", num_floors, 8))

    def simulate(self):
        while True:
            print("Enter 'call <lift_name> <floor>' to call a lift")
            print("Enter 'enter <lift_name> <passenger>' to enter a lift")
            print("Enter 'exit <lift_name> <passenger>' to exit a lift")
            print("Enter 'quit' to exit the simulation")
            command = input("Enter command: ").split()
            if command[0] == 'call':
                if len(command) != 3:
                    print("Invalid command")
                    continue
                lift_name, floor = command[1], int(command[2])
                lift = next((l for l in self.lifts if l.name == lift_name), None)
                if lift:
                    lift.call_lift(floor)
                else:
                    print(f"Lift {lift_name} not found")
            elif command[0] == 'enter':
                if len(command) != 3:
                    print("Invalid command")
                    continue
                lift_name, passenger = command[1], command[2]
                lift = next((l for l in self.lifts if l.name == lift_name), None)
                if lift:
                    lift.enter_lift(passenger)
                else:
                    print(f"Lift {lift_name} not found")
            elif command[0] == 'exit':
                if len(command) != 3:
                    print("Invalid command")
                    continue
                lift_name, passenger = command[1], command[2]
                lift = next((l for l in self.lifts if l.name == lift_name), None)
                if lift:
                    lift.exit_lift(passenger)
                else:
                    print(f"Lift {lift_name} not found")
            elif command[0] == 'quit':
                break
            else:
                print("Invalid command")


simulator = SkyscraperSimulator(20, 4)
simulator.simulate()