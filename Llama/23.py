import csv
from datetime import datetime

class Workout:
    def __init__(self, name, exercise, set, reps, weight):
        self.name = name
        self.exercise = exercise
        self.set = set
        self.reps = reps
        self.weight = weight
        self.date = datetime.now()

class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def import_from_csv(self, filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                name, exercise, set, reps, weight, date = row
                workout = Workout(name, exercise, int(set), int(reps), float(weight), datetime.strptime(date, '%Y-%m-%d'))
                self.add_workout(workout)

    def export_to_csv(self, filename):
        with open(filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Exercise', 'Set', 'Reps', 'Weight', 'Date'])
            for workout in self.workouts:
                writer.writerow([workout.name, workout.exercise, workout.set, workout.reps, workout.weight, workout.date.strftime('%Y-%m-%d')])

def main():
    tracker = WorkoutTracker()
    tracker.import_from_csv('data.csv')
    tracker.export_to_csv('output.csv')

if __name__ == '__main__':
    main()