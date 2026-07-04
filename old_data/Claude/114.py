import datetime
import os
import json

class WorkoutTracker:
    def __init__(self):
        self.workouts = []
        self.data_dir = "workout_data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def import_data(self, filename):
        with open(filename, "r") as f:
            data = json.load(f)
        for workout in data:
            self.workouts.append(workout)

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        for workout in self.workouts:
            print(workout)

    def save_data(self):
        filename = os.path.join(self.data_dir, f"{datetime.datetime.now().strftime('%Y-%m-%d')}.json")
        with open(filename, "w") as f:
            json.dump(self.workouts, f)

class Workout:
    def __init__(self, date, activity, duration, distance, calories):
        self.date = date
        self.activity = activity
        self.duration = duration
        self.distance = distance
        self.calories = calories

    def __str__(self):
        return f"{self.date}: {self.activity} ({self.duration} min, {self.distance} km, {self.calories} calories)"