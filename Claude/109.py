import requests
import json

class WorkoutTracker:
    def __init__(self, api_keys):
        self.api_keys = api_keys

    def import_data(self, app_name, user_id):
        if app_name == 'Fitbit':
            self.import_from_fitbit(user_id)
        elif app_name == 'Apple Health':
            self.import_from_apple_health(user_id)
        elif app_name == 'Google Fit':
            self.import_from_google_fit(user_id)
        else:
            print(f'Unsupported app: {app_name}')

    def import_from_fitbit(self, user_id):
        url = f'https://api.fitbit.com/1/user/{user_id}/activities.json'
        headers = {'Authorization': f'Bearer {self.api_keys["fitbit"]}'}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        
        print(data)

    def import_from_apple_health(self, user_id):
        url = f'https://api.apple.com/health/v1/user/{user_id}/activities'
        headers = {'Authorization': f'Bearer {self.api_keys["apple_health"]}'}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        
        print(data)

    def import_from_google_fit(self, user_id):
        url = f'https://www.googleapis.com/fitness/v1/users/{user_id}/dataset'
        headers = {'Authorization': f'Bearer {self.api_keys["google_fit"]}'}
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        
        print(data)


api_keys = {
    'fitbit': 'your_fitbit_api_key',
    'apple_health': 'your_apple_health_api_key',
    'google_fit': 'your_google_fit_api_key'
}

tracker = WorkoutTracker(api_keys)
tracker.import_data('Fitbit', 'your_fitbit_user_id')
tracker.import_data('Apple Health', 'your_apple_health_user_id')
tracker.import_data('Google Fit', 'your_google_fit_user_id')