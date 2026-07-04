import pandas as pd
from datetime import datetime
import csv

class Workout:
    def __init__(self, name, type, distance, time):
        self.name = name
        self.type = type
        self.distance = distance
        self.time = time

class FitnessApp:
    def __init__(self):
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def import_from_csv(self, file_path):
        workouts = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                name = row[0]
                type = row[1]
                distance = float(row[2])
                time = float(row[3])
                workout = Workout(name, type, distance, time)
                workouts.append(workout)
        return workouts

    def import_from_fitness_app(self, data):
        for entry in data:
            name = entry['name']
            type = entry['type']
            distance = entry['distance']
            time = entry['time']
            workout = Workout(name, type, distance, time)
            self.add_workout(workout)

class User:
    def __init__(self, name):
        self.name = name
        self.app = FitnessApp()

def main():
    user_name = input("Enter your name: ")
    user = User(user_name)
    file_path = input("Enter the CSV file path: ")
    workouts = user.app.import_from_csv(file_path)

    for i, workout in enumerate(workouts):
        print(f"Workout {i+1}:")
        print(f"Name: {workout.name}")
        print(f"Type: {workout.type}")
        print(f"Distance: {workout.distance} km")
        print(f"Time: {workout.time} hours")

    data = [
        {'name': 'John Doe', 'type': 'Running', 'distance': 10, 'time': 2},
        {'name': 'Jane Smith', 'type': 'Cycling', 'distance': 20, 'time': 3}
    ]
    user.app.import_from_fitness_app(data)

if __name__ == "__main__":
    main()