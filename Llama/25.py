import random
import time

class Lift:
    def __init__(self, name):
        self.name = name
        self.location = 'Ground Floor'
        self.capacity = random.randint(1, 10)
        self.status = 'Idle'

    def move(self, direction):
        if direction == 'up':
            self.location = 'Upper Floors'
        elif direction == 'down':
            self.location = 'Lower Floors'
        else:
            print('Invalid direction')

    def is_full(self):
        return len([lift for lift in lifts if lift not in [l for l in lifts if l.name != self.name]]) >= self.capacity

class Skyscraper:
    def __init__(self, num_lifts):
        self.lifts = []
        for i in range(num_lifts):
            self.lifts.append(Lift(f'Lift {i+1}'))

    def simulate(self):
        while True:
            time.sleep(0.5)
            for lift in self.lifts:
                if lift.status == 'Idle' and not lift.is_full():
                    direction = random.choice(['up', 'down'])
                    lift.move(direction)
                    print(f'{lift.name} is moving {direction}')
                elif lift.status == 'Moving':
                    direction = random.choice(['stop', 'up', 'down'])
                    lift.move(direction)
                    if direction != 'Moving':
                        lift.status = 'Idle'
                    print(f'{lift.name} is moving {direction}')

lifts = Skyscraper(10)
lifts.simulate()