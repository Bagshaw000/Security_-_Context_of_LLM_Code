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

    def export_data(self, file_path):
        with open(file_path, 'w') as file:
            json.dump({'workouts': self.workouts}, file)

    def display_workouts(self):
        for workout in self.workouts:
            print(workout)

if __name__ == "__main__":
    tracker = WorkoutTracker()
    tracker.import_data('workouts.json')
    tracker.display_workouts()
    tracker.export_data('exported_workouts.json')