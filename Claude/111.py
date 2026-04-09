import pandas as pd
from datetime import datetime

class WorkoutTracker:
    def __init__(self, user_id):
        self.user_id = user_id
        self.workout_data = pd.DataFrame(columns=['date', 'activity', 'duration', 'distance', 'calories'])

    def import_data(self, file_path):
        file_type = file_path.split('.')[-1]
        if file_type == 'csv':
            new_data = pd.read_csv(file_path)
        elif file_type == 'xlsx':
            new_data = pd.read_excel(file_path)
        else:
            raise ValueError('Unsupported file type. Please provide a CSV or XLSX file.')

        self.workout_data = pd.concat([self.workout_data, new_data], ignore_index=True)

    def add_workout(self, date, activity, duration, distance, calories):
        new_workout = pd.DataFrame({'date': [date], 'activity': [activity], 'duration': [duration], 'distance': [distance], 'calories': [calories]})
        self.workout_data = pd.concat([self.workout_data, new_workout], ignore_index=True)

    def view_workouts(self, start_date=None, end_date=None):
        if start_date and end_date:
            filtered_data = self.workout_data[(self.workout_data['date'] >= start_date) & (self.workout_data['date'] <= end_date)]
        else:
            filtered_data = self.workout_data
        return filtered_data

    def get_summary(self, start_date=None, end_date=None):
        filtered_data = self.view_workouts(start_date, end_date)
        total_duration = filtered_data['duration'].sum()
        total_distance = filtered_data['distance'].sum()
        total_calories = filtered_data['calories'].sum()
        return {'total_duration': total_duration, 'total_distance': total_distance, 'total_calories': total_calories}