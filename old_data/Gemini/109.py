import json
import unittest
from abc import ABC, abstractmethod
from datetime import datetime

class Exercise:
    
    def __init__(self, name, sets, reps, weight_kg=None):
        self.name = name
        self.sets = sets
        self.reps = reps
        self.weight_kg = weight_kg

    def __repr__(self):
        return f"{self.name}: {self.sets}x{self.reps} @ {self.weight_kg or 0}kg"

class Workout:
    
    def __init__(self, timestamp, activity_type, source="Manual"):
        self.timestamp = timestamp
        self.activity_type = activity_type
        self.source = source
        self.exercises = []

    def add_exercise(self, name, sets, reps, weight_kg=None):
        exercise = Exercise(name, sets, reps, weight_kg)
        self.exercises.append(exercise)

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "activity_type": self.activity_type,
            "source": self.source,
            "exercises": [vars(e) for e in self.exercises]
        }

class FitnessDataImporter(ABC):
    
    @abstractmethod
    def parse_data(self, raw_input: str) -> Workout:
        pass

class StravaImporter(FitnessDataImporter):
    
    def parse_data(self, raw_input: str) -> Workout:
        data = json.loads(raw_input)
        
        workout = Workout(
            timestamp=data.get("start_date_local"),
            activity_type=data.get("type"),
            source="Strava"
        )
        return workout

class FitbitImporter(FitnessDataImporter):
    
    def parse_data(self, raw_input: str) -> Workout:
        data = json.loads(raw_input)
        workout = Workout(
            timestamp=data.get("startTime"),
            activity_type=data.get("activityName"),
            source="Fitbit"
        )
        return workout

class WorkoutTrackerApp:
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.workouts = []

    def log_workout(self, workout: Workout):
        self.workouts.append(workout)
        print(f"Logged {workout.activity_type} session from {workout.source}.")

    def import_from_provider(self, importer: FitnessDataImporter, raw_data: str):
        try:
            workout = importer.parse_data(raw_data)
            self.log_workout(workout)
            return True
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error importing data: {e}")
            return False

    def sync_to_aws(self):
        
        payload = json.dumps([w.to_dict() for w in self.workouts])
        print(f"Uploading {len(payload)} bytes to AWS S3 bucket 'workout-tracker-storage'...")
        
        return True

class TestWorkoutTracker(unittest.TestCase):
    
    def setUp(self):
        self.app = WorkoutTrackerApp(user_id="john_bristol_2023")

    def test_manual_entry(self):
        w = Workout(datetime.now().isoformat(), "Strength")
        w.add_exercise("Deadlift", 3, 5, 120)
        self.app.log_workout(w)
        self.assertEqual(len(self.app.workouts), 1)
        self.assertEqual(self.app.workouts[0].exercises[0].name, "Deadlift")

    def test_strava_import_logic(self):
        raw_json = '{"start_date_local": "2023-11-01T14:00:00Z", "type": "Run"}'
        importer = StravaImporter()
        success = self.app.import_external_data_via_logic(importer, raw_json)
        self.assertTrue(success)
        self.assertEqual(self.app.workouts[0].source, "Strava")

    def import_external_data_via_logic(self, importer, data):
        
        return self.app.import_from_provider(importer, data)

if __name__ == "__main__":
    
    app = WorkoutTrackerApp(user_id="j_smith_dev")

    
    leg_day = Workout(datetime.now().isoformat(), "Hypertrophy")
    leg_day.add_exercise("Squat", 4, 8, 100)
    leg_day.add_exercise("Leg Press", 3, 12, 200)
    app.log_workout(leg_day)

    
    strava_json_data = '{"start_date_local": "2023-11-02T08:15:00Z", "type": "Run"}'
    app.import_from_provider(StravaImporter(), strava_json_data)

    
    app.sync_to_aws()

    
    print("\nStarting Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWorkoutTracker)
    unittest.TextTestRunner(verbosity=1).run(suite)