import datetime
import json
from typing import List, Tuple

class WorkoutEntry:
    def __init__(self, activity: str, duration: int, distance: float, calories: float, date: datetime.date):
        self.activity = activity
        self.duration = duration
        self.distance = distance
        self.calories = calories
        self.date = date

class WorkoutTracker:
    def __init__(self):
        self.workouts: List[WorkoutEntry] = []

    def add_workout(self, workout: WorkoutEntry):
        self.workouts.append(workout)

    def import_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for workout_data in data:
                activity = workout_data['activity']
                duration = workout_data['duration']
                distance = workout_data['distance']
                calories = workout_data['calories']
                date = datetime.datetime.strptime(workout_data['date'], '%Y-%m-%d').date()
                workout = WorkoutEntry(activity, duration, distance, calories, date)
                self.add_workout(workout)

    def get_workouts_by_date(self, date: datetime.date) -> List[WorkoutEntry]:
        return [workout for workout in self.workouts if workout.date == date]

    def get_total_distance(self) -> float:
        return sum(workout.distance for workout in self.workouts)

    def get_total_calories(self) -> float:
        return sum(workout.calories for workout in self.workouts)