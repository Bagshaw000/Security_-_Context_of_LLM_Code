import json
import requests

class WorkoutTracker:
    def __init__(self, user_id, api_key):
        self.user_id = user_id
        self.api_key = api_key
        self.workouts = []

    def import_from_fitbit(self, start_date, end_date):
        url = f"https://api.fitbit.com/1/user/{self.user_id}/activities/date/{start_date}/{end_date}.json"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        self.workouts.extend(data["activities"])

    def import_from_strava(self, start_date, end_date):
        url = f"https://www.strava.com/api/v3/athlete/activities?after={start_date}&before={end_date}"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        self.workouts.extend(data)

    def save_workouts(self, filename):
        with open(filename, "w") as f:
            json.dump(self.workouts, f)

    def load_workouts(self, filename):
        with open(filename, "r") as f:
            self.workouts = json.load(f)