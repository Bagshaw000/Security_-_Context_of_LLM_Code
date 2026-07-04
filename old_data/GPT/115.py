import json
import os

class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def import_data(self, file_path):
        if not os.path.exists(file_path):
            print("File not found.")
            return
        
        with open(file_path, 'r') as file:
            data = json.load(file)
            for workout in data.get('workouts', []):
                self.add_workout(workout)

    def display_workouts(self):
        for i, workout in enumerate(self.workouts, start=1):
            print(f"{i}. {workout['date']}: {workout['type']} - {workout['duration']} minutes")

if __name__ == "__main__":
    tracker = WorkoutTracker()
    tracker.import_data('workouts.json')
    tracker.display_workouts()