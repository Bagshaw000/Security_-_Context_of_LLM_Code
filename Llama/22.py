import pandas as pd
from datetime import datetime

class Workout:
    def __init__(self, name, duration, calories_burned):
        self.name = name
        self.duration = duration
        self.calories_burned = calories_burned

class Exercise:
    def __init__(self, name, sets, reps, weight):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight = weight

class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def import_from_fitness_app(self, csv_file):
        df = pd.read_csv(csv_file)
        for index, row in df.iterrows():
            name = row['Name']
            duration = float(row['Duration'])
            calories_burned = int(row['Calories Burned'])
            exercise_name = row['Exercise Name']
            sets = int(row['Sets'])
            reps = int(row['Reps'])
            weight = float(row['Weight'])
            workout = Workout(name, duration, calories_burned)
            exercise = Exercise(exercise_name, sets, reps, weight)
            workout.exercises.append(exercise)

    def display_workouts(self):
        for i, workout in enumerate(self.workouts):
            print(f"Workout {i+1}:")
            print(f"Name: {workout.name}")
            print(f"Duration: {workout.duration} minutes")
            print(f"Calories Burned: {workout.calories_burned}")
            for exercise in workout.exercises:
                print(f"{exercise.name}: {exercise.reps} sets of {exercise.weight} weight")

def main():
    tracker = WorkoutTracker()
    tracker.import_from_fitness_app('fitness_data.csv')
    tracker.display_workouts()

if __name__ == "__main__":
    main()