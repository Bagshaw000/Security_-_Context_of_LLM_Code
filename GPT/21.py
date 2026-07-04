import json
import requests

class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def import_data(self, source_url):
        try:
            response = requests.get(source_url)
            response.raise_for_status()
            data = response.json()
            self.workouts.extend(data['workouts'])
            print("Data imported successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error importing data: {e}")

    def add_workout(self, workout):
        self.workouts.append(workout)
        print("Workout added successfully.")

    def view_workouts(self):
        for workout in self.workouts:
            print(workout)

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            json.dump({'workouts': self.workouts}, f)
        print("Workouts saved to file.")


if __name__ == "__main__":
    tracker = WorkoutTracker()
    tracker.import_data("https://api.example.com/fitness_data")
    tracker.add_workout({"date": "2023-10-01", "type": "Running", "duration": 30, "calories": 300})
    tracker.view_workouts()
    tracker.save_to_file("workouts.json")