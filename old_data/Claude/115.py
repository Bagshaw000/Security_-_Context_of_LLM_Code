import requests
import json

class WorkoutTracker:
    def __init__(self, app_name, api_key):
        self.app_name = app_name
        self.api_key = api_key
        self.data = []

    def import_data(self, app_name, start_date, end_date):
        url = f"https://api.{app_name}.com/workouts?start_date={start_date}&end_date={end_date}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            self.data.extend(response.json())
        else:
            print(f"Error importing data from {app_name}: {response.status_code} - {response.text}")

    def save_data(self, file_name):
        with open(file_name, "w") as f:
            json.dump(self.data, f)

    def load_data(self, file_name):
        with open(file_name, "r") as f:
            self.data = json.load(f)

    def analyze_data(self):
        total_duration = sum(workout["duration"] for workout in self.data)
        total_calories = sum(workout["calories"] for workout in self.data)
        print(f"Total duration: {total_duration} minutes")
        print(f"Total calories burned: {total_calories} calories")