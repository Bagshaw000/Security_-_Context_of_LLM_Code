class Workout:
    def __init__(self, date, duration, type, calories_burned):
        self.date = date
        self.duration = duration  
        self.type = type
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.type} for {self.duration} mins, Calories burned: {self.calories_burned}"


class WorkoutTracker:
    def __init__(self):
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def import_data(self, data):
        for entry in data:
            workout = Workout(entry['date'], entry['duration'], entry['type'], entry['calories_burned'])
            self.add_workout(workout)

    def display_workouts(self):
        for workout in self.workouts:
            print(workout)



if __name__ == "__main__":
    tracker = WorkoutTracker()

    
    imported_data = [
        {'date': '2023-10-01', 'duration': 30, 'type': 'Running', 'calories_burned': 300},
        {'date': '2023-10-02', 'duration': 45, 'type': 'Cycling', 'calories_burned': 400},
        {'date': '2023-10-03', 'duration': 60, 'type': 'Swimming', 'calories_burned': 500},
    ]

    tracker.import_data(imported_data)
    tracker.display_workouts()