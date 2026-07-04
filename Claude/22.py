import datetime
import csv
import json
import requests

class WorkoutTracker:
    def __init__(self, user_name):
        self.user_name = user_name
        self.workouts = []

    def import_data(self, app_name, api_key):
        if app_name == 'Fitbit':
            self.import_fitbit_data(api_key)
        elif app_name == 'Strava':
            self.import_strava_data(api_key)
        elif app_name == 'Apple Health':
            self.import_apple_health_data(api_key)

    def import_fitbit_data(self, api_key):
        url = 'https://api.fitbit.com/1/user/-/activities/list.json'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        data = response.json()
        for activity in data['activities']:
            workout = {
                'name': activity['name'],
                'duration': activity['duration'],
                'distance': activity['distance'],
                'date': datetime.datetime.strptime(activity['startTime'], '%Y-%m-%dT%H:%M:%S.%f%z').date()
            }
            self.workouts.append(workout)

    def import_strava_data(self, api_key):
        url = 'https://www.strava.com/api/v3/athlete/activities'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        data = response.json()
        for activity in data:
            workout = {
                'name': activity['name'],
                'duration': activity['moving_time'],
                'distance': activity['distance'],
                'date': datetime.datetime.strptime(activity['start_date'], '%Y-%m-%dT%H:%M:%SZ').date()
            }
            self.workouts.append(workout)

    def import_apple_health_data(self, api_key):
        url = 'https://api.apple-healthkit.com/v1/workouts'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        data = response.json()
        for workout in data['workouts']:
            new_workout = {
                'name': workout['activityType'],
                'duration': workout['duration'],
                'distance': workout['distance'],
                'date': datetime.datetime.fromtimestamp(workout['startDate']).date()
            }
            self.workouts.append(new_workout)

    def export_to_csv(self, file_name):
        with open(file_name, 'w', newline='') as csvfile:
            fieldnames = ['name', 'duration', 'distance', 'date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for workout in self.workouts:
                writer.writerow(workout)

    def export_to_json(self, file_name):
        with open(file_name, 'w') as jsonfile:
            json.dump({'user_name': self.user_name, 'workouts': self.workouts}, jsonfile, indent=4)