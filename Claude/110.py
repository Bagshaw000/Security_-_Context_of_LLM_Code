import datetime

class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def add_workout(self, workout_type, duration, distance, calories):
        workout = {
            'type': workout_type,
            'duration': duration,
            'distance': distance,
            'calories': calories,
            'date': datetime.datetime.now().strftime('%Y-%m-%d')
        }
        self.workouts.append(workout)

    def import_data(self, file_path):
        with open(file_path, 'r') as file:
            data = file.readlines()
        for line in data:
            workout_data = line.strip().split(',')
            workout_type, duration, distance, calories = workout_data
            self.add_workout(workout_type, float(duration), float(distance), float(calories))

    def get_workouts(self):
        return self.workouts

    def get_total_distance(self):
        total_distance = sum(workout['distance'] for workout in self.workouts)
        return total_distance

    def get_total_calories(self):
        total_calories = sum(workout['calories'] for workout in self.workouts)
        return total_calories