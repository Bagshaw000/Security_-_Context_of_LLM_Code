import datetime
import json
import requests

class WorkoutTracker:
    def __init__(self, user_id, api_key):
        self.user_id = user_id
        self.api_key = api_key
        self.workouts = []

    def import_from_fitbit(self, start_date, end_date):
        url = f"https://api.fitbit.com/1/user/{self.user_id}/activities/date/{start_date}/{end_date}.json"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        data = response.json()
        for activity in data["activities"]:
            self.workouts.append({
                "name": activity["activityName"],
                "duration": activity["duration"],
                "calories": activity["calories"],
                "date": activity["startTime"].split("T")[0]
            })

    def import_from_strava(self, access_token, start_date, end_date):
        url = f"https://www.strava.com/api/v3/athlete/activities?after={start_date}&before={end_date}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        activities = response.json()
        for activity in activities:
            self.workouts.append({
                "name": activity["name"],
                "duration": activity["moving_time"],
                "calories": activity["calories"],
                "date": datetime.datetime.fromtimestamp(activity["start_date_local"]).strftime("%Y-%m-%d")
            })

    def save_workouts(self, filename):
        with open(filename, "w") as f:
            json.dump(self.workouts, f)

    def load_workouts(self, filename):
        with open(filename, "r") as f:
            self.workouts = json.load(f)