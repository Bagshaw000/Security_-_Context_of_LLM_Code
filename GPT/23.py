class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def import_data(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                date, type_of_workout, duration = line.strip().split(',')
                self.workouts.append({
                    'date': date,
                    'type': type_of_workout,
                    'duration': int(duration)
                })

    def display_workouts(self):
        for workout in self.workouts:
            print(f"Date: {workout['date']}, Type: {workout['type']}, Duration: {workout['duration']} minutes")


tracker = WorkoutTracker()
tracker.import_data('workouts.csv')
tracker.display_workouts()