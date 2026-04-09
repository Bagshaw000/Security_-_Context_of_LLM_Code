import json
import requests

class WorkoutTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.data = {}

    def import_data(self, app_name, access_token):
        if app_name == 'Fitbit':
            self.import_fitbit_data(access_token)
        elif app_name == 'Strava':
            self.import_strava_data(access_token)
        elif app_name == 'Apple Health':
            self.import_apple_health_data(access_token)

    def import_fitbit_data(self, access_token):
        url = f'https://api.fitbit.com/1/user/{self.user_id}/activities.json'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)
        self.data['Fitbit'] = response.json()

    def import_strava_data(self, access_token):
        url = 'https://www.strava.com/api/v3/athlete/activities'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)
        self.data['Strava'] = response.json()

    def import_apple_health_data(self, access_token):
        
        pass

    def save_data(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.data, f)

    def load_data(self, filename):
        with open(filename, 'r') as f:
            self.data = json.load(f)