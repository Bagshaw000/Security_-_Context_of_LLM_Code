import json
import requests

class WorkoutTracker:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.fitness-app.com"

    def import_data(self, app_name, user_id):
        url = f"{self.base_url}/import/{app_name}/{user_id}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        return json.loads(response.text)

    def log_workout(self, workout_data):
        url = f"{self.base_url}/workouts"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        response = requests.post(url, headers=headers, json=workout_data)
        return json.loads(response.text)

    def view_workouts(self, start_date=None, end_date=None):
        url = f"{self.base_url}/workouts"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        response = requests.get(url, headers=headers, params=params)
        return json.loads(response.text)