import json
import boto3
from abc import ABC, abstractmethod
from datetime import datetime
from botocore.exceptions import ClientError

class Workout:
    
    def __init__(self, exercise_name, sets, reps, weight_kg, date=None):
        self.exercise_name = exercise_name
        self.sets = sets
        self.reps = reps
        self.weight_kg = weight_kg
        self.date = date or datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "exercise_name": self.exercise_name,
            "sets": self.sets,
            "reps": self.reps,
            "weight_kg": self.weight_kg,
            "date": self.date
        }

class BaseImporter(ABC):
    
    @abstractmethod
    def transform(self, raw_data):
        pass

class StravaImporter(BaseImporter):
    
    def transform(self, raw_data):
        workouts = []
        for activity in raw_data.get("activities", []):
            
            workouts.append(Workout(
                exercise_name=activity.get("type", "Unknown"),
                sets=1,
                reps=0,
                weight_kg=0,
                date=activity.get("start_date")
            ))
        return workouts

class MyFitnessPalImporter(BaseImporter):
    
    def transform(self, raw_data):
        workouts = []
        for entry in raw_data.get("exercises", []):
            workouts.append(Workout(
                exercise_name=entry.get("name"),
                sets=entry.get("sets", 0),
                reps=entry.get("reps", 0),
                weight_kg=entry.get("weight", 0),
                date=entry.get("date")
            ))
        return workouts

class WorkoutTrackerApp:
    
    def __init__(self, bucket_name, region_name='us-east-1'):
        self.workouts = []
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.bucket_name = bucket_name

    def add_workout(self, workout):
        if not isinstance(workout, Workout):
            raise ValueError("Invalid workout object")
        self.workouts.append(workout)

    def import_external_data(self, importer: BaseImporter, raw_data):
        
        new_workouts = importer.transform(raw_data)
        self.workouts.extend(new_workouts)
        print(f"Successfully imported {len(new_workouts)} workouts.")

    def save_to_s3(self, filename="workout_history.json"):
        
        try:
            data = json.dumps([w.to_dict() for w in self.workouts])
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=data
            )
            return True
        except ClientError as e:
            print(f"AWS Error: {e}")
            return False

import unittest
from unittest.mock import MagicMock

class TestWorkoutTracker(unittest.TestCase):
    def setUp(self):
        self.app = WorkoutTrackerApp(bucket_name="test-fitness-bucket")
        self.app.s3_client = MagicMock() 

    def test_add_workout(self):
        workout = Workout("Bench Press", 3, 10, 80)
        self.app.add_workout(workout)
        self.assertEqual(len(self.app.workouts), 1)
        self.assertEqual(self.app.workouts[0].exercise_name, "Bench Press")

    def test_strava_import(self):
        mock_strava_data = {
            "activities": [
                {"type": "Run", "start_date": "2023-10-01T08:00:00Z"},
                {"type": "WeightTraining", "start_date": "2023-10-02T17:00:00Z"}
            ]
        }
        importer = StravaImporter()
        self.app.import_external_data(importer, mock_strava_data)
        self.assertEqual(len(self.app.workouts), 2)
        self.assertEqual(self.app.workouts[0].exercise_name, "Run")

    def test_save_to_s3_success(self):
        self.app.s3_client.put_object.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
        result = self.app.save_to_s3()
        self.assertTrue(result)
        self.app.s3_client.put_object.assert_called_once()

if __name__ == "__main__":
    
    app = WorkoutTrackerApp(bucket_name="my-fitness-data-storage")
    
    
    app.add_workout(Workout("Deadlift", 5, 5, 140))
    
    
    mfp_data = {
        "exercises": [
            {"name": "Squat", "sets": 3, "reps": 12, "weight": 100, "date": "2023-10-05"}
        ]
    }
    app.import_external_data(MyFitnessPalImporter(), mfp_data)
    
    print(f"Total workouts tracked: {len(app.workouts)}")
    
    
    unittest.main()