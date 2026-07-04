import json
import csv

class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def add_workout(self, date, type, duration, calories):
        workout = {
            'date': date,
            'type': type,
            'duration': duration,
            'calories': calories
        }
        self.workouts.append(workout)

    def import_from_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for entry in data:
                self.add_workout(entry['date'], entry['type'], entry['duration'], entry['calories'])

    def import_from_csv(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.add_workout(row['date'], row['type'], row['duration'], row['calories'])

    def display_workouts(self):
        for workout in self.workouts:
            print(f"Date: {workout['date']}, Type: {workout['type']}, Duration: {workout['duration']} mins, Calories: {workout['calories']}")


tracker = WorkoutTracker()
tracker.import_from_json('workouts.json')
tracker.import_from_csv('workouts.csv')
tracker.display_workouts()