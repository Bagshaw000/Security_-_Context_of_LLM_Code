import json
import requests

class WorkoutTracker:
    def __init__(self, user_id, api_key):
        self.user_id = user_id
        self.api_key = api_key
        self.base_url = "https://api.example.com/v1"

    def import_data(self, app_name):
        if app_name == "Fitbit":
            self.import_fitbit_data()
        elif app_name == "Strava":
            self.import_strava_data()
        elif app_name == "Apple Health":
            self.import_apple_health_data()
        else:
            print(f"Unsupported app: {app_name}")

    def import_fitbit_data(self):
        url = f"{self.base_url}/fitbit/activities"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        
        print("Fitbit data imported successfully.")

    def import_strava_data(self):
        url = f"{self.base_url}/strava/activities"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        
        print("Strava data imported successfully.")

    def import_apple_health_data(self):
        url = f"{self.base_url}/apple-health/activities"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        
        print("Apple Health data imported successfully.")


tracker = WorkoutTracker("user123", "abc123")
tracker.import_data("Fitbit")
tracker.import_data("Strava")
tracker.import_data("Apple Health")