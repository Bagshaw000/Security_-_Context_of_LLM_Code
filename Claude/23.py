import csv
from datetime import datetime

class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def import_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    workout = {
                        'date': datetime.strptime(row['date'], '%Y-%m-%d'),
                        'activity': row['activity'],
                        'duration': float(row['duration']),
                        'calories': float(row['calories'])
                    }
                    self.workouts.append(workout)
            print(f'Successfully imported {len(self.workouts)} workouts.')
        except FileNotFoundError:
            print('Error: File not found.')
        except (ValueError, KeyError):
            print('Error: Invalid data format in the file.')

    def get_total_duration(self):
        total_duration = sum(workout['duration'] for workout in self.workouts)
        return total_duration

    def get_total_calories(self):
        total_calories = sum(workout['calories'] for workout in self.workouts)
        return total_calories

    def get_workouts_by_activity(self, activity):
        return [workout for workout in self.workouts if workout['activity'] == activity]

    def get_workouts_by_date(self, date):
        return [workout for workout in self.workouts if workout['date'].date() == date.date()]


tracker = WorkoutTracker()
tracker.import_data('fitness_data.csv')
print(f'Total duration: {tracker.get_total_duration()} minutes')
print(f'Total calories: {tracker.get_total_calories()} calories')

print('Workouts by activity:')
for activity, workouts in [(activity, tracker.get_workouts_by_activity(activity)) for activity in set(workout['activity'] for workout in tracker.workouts)]:
    print(f'{activity}: {len(workouts)} workouts')

print('Workouts by date:')
for date in set(workout['date'].date() for workout in tracker.workouts):
    workouts = tracker.get_workouts_by_date(date)
    print(f'{date}: {len(workouts)} workouts')