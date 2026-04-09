import json
import uuid
import unittest
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any

class Workout:
    
    def __init__(self, activity_type: str, duration_mins: int, distance_km: float, timestamp: datetime):
        self.workout_id = str(uuid.uuid4())
        self.activity_type = activity_type
        self.duration_mins = duration_mins
        self.distance_km = distance_km
        self.timestamp = timestamp

    def to_dynamo_item(self) -> Dict[str, Any]:
        
        return {
            'WorkoutID': {'S': self.workout_id},
            'ActivityType': {'S': self.activity_type},
            'Duration': {'N': str(self.duration_mins)},
            'Distance': {'N': str(self.distance_km)},
            'Timestamp': {'S': self.timestamp.isoformat()}
        }

class FitnessDataImporter(ABC):
    
    @abstractmethod
    def fetch_workouts(self, source_identifier: str) -> List[Workout]:
        pass

class StravaImporter(FitnessDataImporter):
    
    def fetch_workouts(self, source_identifier: str) -> List[Workout]:
        
        
        
        mock_raw_data = [
            {"type": "Run", "mins": 45, "km": 8.2, "date": "2023-10-15T07:30:00"},
            {"type": "Cycle", "mins": 120, "km": 45.0, "date": "2023-10-16T10:00:00"}
        ]
        
        workouts = []
        for item in mock_raw_data:
            workouts.append(Workout(
                activity_type=item["type"],
                duration_mins=item["mins"],
                distance_km=item["km"],
                timestamp=datetime.fromisoformat(item["date"])
            ))
        return workouts

class GarminImporter(FitnessDataImporter):
    
    def fetch_workouts(self, source_identifier: str) -> List[Workout]:
        mock_raw_data = [
            {"act": "Swimming", "dur": 30, "dist": 1.5, "ts": "2023-10-17T18:00:00"}
        ]
        
        workouts = []
        for item in mock_raw_data:
            workouts.append(Workout(
                activity_type=item["act"],
                duration_mins=item["dur"],
                distance_km=item["dist"],
                timestamp=datetime.fromisoformat(item["ts"])
            ))
        return workouts

class WorkoutTrackerService:
    
    def __init__(self, db_client=None):
        
        self.db_client = db_client
        self.workout_history = []

    def import_external_data(self, importer: FitnessDataImporter, source: str):
        new_workouts = importer.fetch_workouts(source)
        for workout in new_workouts:
            self.workout_history.append(workout)
            self._save_to_cloud(workout)
        return len(new_workouts)

    def _save_to_cloud(self, workout: Workout):
        
        if self.db_client:
            print(f"Pushing workout {workout.workout_id} to AWS DynamoDB...")
            

class TestWorkoutApp(unittest.TestCase):
    
    def setUp(self):
        self.service = WorkoutTrackerService()

    def test_strava_import_count(self):
        importer = StravaImporter()
        count = self.service.import_external_data(importer, "mock_token")
        self.assertEqual(count, 2)
        self.assertEqual(self.service.workout_history[0].activity_type, "Run")

    def test_garmin_import_count(self):
        importer = GarminImporter()
        count = self.service.import_external_data(importer, "mock_token")
        self.assertEqual(count, 1)
        self.assertEqual(self.service.workout_history[0].activity_type, "Swimming")

    def test_workout_formatting(self):
        dt = datetime.now()
        workout = Workout("Yoga", 60, 0.0, dt)
        dynamo_data = workout.to_dynamo_item()
        self.assertEqual(dynamo_data['ActivityType']['S'], "Yoga")
        self.assertEqual(dynamo_data['Duration']['N'], "60")

if __name__ == "__main__":
    
    app_service = WorkoutTrackerService()
    
    print("Starting Workout Tracker Import Process...")
    
    strava_provider = StravaImporter()
    garmin_provider = GarminImporter()
    
    s_count = app_service.import_external_data(strava_provider, "user_auth_token_123")
    g_count = app_service.import_external_data(garmin_provider, "user_auth_token_456")
    
    print(f"Imported {s_count} activities from Strava.")
    print(f"Imported {g_count} activities from Garmin.")
    print(f"Total workouts in local state: {len(app_service.workout_history)}")

    
    print("\nRunning Unit Tests...")
    unittest.main()