import pandas as pd
from datetime import datetime

class WorkoutTracker:
    def __init__(self):
        self.workouts = pd.DataFrame(columns=['Date', 'Activity', 'Duration', 'Calories'])

    def import_data(self, file_path):
        data = pd.read_csv(file_path)
        self.workouts = pd.concat([self.workouts, data], ignore_index=True)
        print(f'{len(data)} workouts imported successfully.')

    def add_workout(self, date, activity, duration, calories):
        new_workout = pd.DataFrame({'Date': [date], 'Activity': [activity], 'Duration': [duration], 'Calories': [calories]})
        self.workouts = pd.concat([self.workouts, new_workout], ignore_index=True)
        print(f'New workout added: {activity} on {date}.')

    def view_workouts(self, start_date=None, end_date=None):
        if start_date and end_date:
            filtered = self.workouts[(self.workouts['Date'] >= start_date) & (self.workouts['Date'] <= end_date)]
        else:
            filtered = self.workouts
        print(filtered)

    def get_total_calories(self, start_date=None, end_date=None):
        if start_date and end_date:
            filtered = self.workouts[(self.workouts['Date'] >= start_date) & (self.workouts['Date'] <= end_date)]
        else:
            filtered = self.workouts
        return filtered['Calories'].sum()

    def get_total_duration(self, start_date=None, end_date=None):
        if start_date and end_date:
            filtered = self.workouts[(self.workouts['Date'] >= start_date) & (self.workouts['Date'] <= end_date)]
        else:
            filtered = self.workouts
        return filtered['Duration'].sum()