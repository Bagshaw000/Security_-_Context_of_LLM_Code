import pandas as pd
from datetime import datetime

class WorkoutTracker:
    def __init__(self):
        self.data = pd.DataFrame(columns=['Date', 'Activity', 'Duration', 'Calories'])

    def import_data(self, file_path):
        try:
            imported_data = pd.read_csv(file_path)
            self.data = pd.concat([self.data, imported_data], ignore_index=True)
            print(f"Data imported from {file_path}")
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except pd.errors.ParserError:
            print("Error: Incorrect file format")

    def add_workout(self, date, activity, duration, calories):
        new_row = {'Date': date, 'Activity': activity, 'Duration': duration, 'Calories': calories}
        self.data = self.data.append(new_row, ignore_index=True)
        print("Workout added successfully.")

    def view_workouts(self):
        print(self.data)

    def analyze_data(self):
        print("Workout Analysis:")
        print(f"Total Workouts: {len(self.data)}")
        print(f"Total Calories Burned: {self.data['Calories'].sum()}")
        print(f"Average Workout Duration: {self.data['Duration'].mean()} minutes")