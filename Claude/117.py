import datetime
import requests

class WorkoutTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.workouts = []

    def import_data(self, app_name, api_key):
        if app_name == 'Fitbit':
            self.import_fitbit_data(api_key)
        elif app_name == 'Strava':
            self.import_strava_data(api_key)
        else:
            print(f'Unsupported app: {app_name}')

    def import_fitbit_data(self, api_key):
        url = f'https://api.fitbit.com/1/user/{self.user_id}/activities.json'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        data = response.json()
        for activity in data['activities']:
            workout = {
                'name': activity['name'],
                'start_time': datetime.datetime.strptime(activity['startTime'], '%Y-%m-%dT%H:%M:%S.%f%z'),
                'duration': activity['duration'],
                'calories': activity['calories'],
                'distance': activity['distance']
            }
            self.workouts.append(workout)

    def import_strava_data(self, api_key):
        url = f'https://www.strava.com/api/v3/athlete/activities'
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.get(url, headers=headers)
        data = response.json()
        for activity in data:
            workout = {
                'name': activity['name'],
                'start_time': datetime.datetime.strptime(activity['start_date_local'], '%Y-%m-%dT%H:%M:%S%z'),
                'duration': activity['moving_time'],
                'calories': activity['calories'],
                'distance': activity['distance']
            }
            self.workouts.append(workout)

    def view_workouts(self):
        for workout in self.workouts:
            print(f"Name: {workout['name']}")
            print(f"Start Time: {workout['start_time']}")
            print(f"Duration: {workout['duration']} seconds")
            print(f"Calories: {workout['calories']} calories")
            print(f"Distance: {workout['distance']} meters")
            print()