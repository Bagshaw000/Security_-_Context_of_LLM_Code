import datetime

class Workout:
    def __init__(self, name, date, duration, calories_burned, distance):
        self.name = name
        self.date = date
        self.duration = duration
        self.calories_burned = calories_burned
        self.distance = distance

class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def import_data(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                data = line.strip().split(',')
                name, date, duration, calories_burned, distance = data
                workout = Workout(name, datetime.datetime.strptime(date, '%Y-%m-%d'), float(duration), float(calories_burned), float(distance))
                self.add_workout(workout)

    def get_total_calories_burned(self):
        total_calories = sum(workout.calories_burned for workout in self.workouts)
        return total_calories

    def get_total_distance(self):
        total_distance = sum(workout.distance for workout in self.workouts)
        return total_distance

    def get_workouts_by_date(self, date):
        return [workout for workout in self.workouts if workout.date.date() == date.date()]