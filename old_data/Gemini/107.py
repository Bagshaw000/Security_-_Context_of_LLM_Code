import json
from abc import ABC, abstractmethod
from datetime import datetime
import unittest

class Workout:
    def __init__(self, activity_type, duration_minutes, calories, source, timestamp=None):
        self.activity_type = activity_type
        self.duration_minutes = duration_minutes
        self.calories = calories
        self.source = source
        self.timestamp = timestamp or datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            'activity_type': self.activity_type,
            'duration_minutes': self.duration_minutes,
            'calories': self.calories,
            'source': self.source,
            'timestamp': self.timestamp
        }

class ExternalAppImporter(ABC):
    @abstractmethod
    def transform(self, raw_data):
        pass

class StravaImporter(ExternalAppImporter):
    def transform(self, raw_data):
        
        data = json.loads(raw_data)
        return Workout(
            activity_type=data.get('type', 'Unknown'),
            duration_minutes=round(data.get('moving_time', 0) / 60, 2),
            calories=data.get('calories', 0),
            source='Strava'
        )

class FitbitImporter(ExternalAppImporter):
    def transform(self, raw_data):
        
        data = json.loads(raw_data)
        return Workout(
            activity_type=data.get('activityName', 'Unknown'),
            duration_minutes=round(data.get('duration', 0) / 60000, 2),
            calories=data.get('calories', 0),
            source='Fitbit'
        )

class WorkoutService:
    def __init__(self, storage_client=None):
        
        self.storage_client = storage_client
        self.local_cache = []

    def import_external_data(self, importer: ExternalAppImporter, payload: str):
        workout = importer.transform(payload)
        self.local_cache.append(workout)
        self._persist_to_aws(workout)
        return workout

    def _persist_to_aws(self, workout):
        
        if self.storage_client:
            try:
                
                
                
                pass
            except Exception as e:
                print(f"Cloud sync failed: {e}")

class TestWorkoutApp(unittest.TestCase):
    def setUp(self):
        self.service = WorkoutService()

    def test_strava_import_logic(self):
        importer = StravaImporter()
        raw_json = '{"type": "Run", "moving_time": 1200, "calories": 250}'
        workout = self.service.import_external_data(importer, raw_json)
        
        self.assertEqual(workout.activity_type, "Run")
        self.assertEqual(workout.duration_minutes, 20.0)
        self.assertEqual(workout.source, "Strava")

    def test_fitbit_import_logic(self):
        importer = FitbitImporter()
        raw_json = '{"activityName": "Walk", "duration": 600000, "calories": 50}'
        workout = self.service.import_external_data(importer, raw_json)
        
        self.assertEqual(workout.activity_type, "Walk")
        self.assertEqual(workout.duration_minutes, 10.0)
        self.assertEqual(workout.source, "Fitbit")

if __name__ == "__main__":
    
    app_service = WorkoutService()
    
    
    sample_strava_data = '{"type": "Ride", "moving_time": 3600, "calories": 600}'
    imported_workout = app_service.import_external_data(StravaImporter(), sample_strava_data)
    
    print(f"Successfully imported {imported_workout.activity_type} from {imported_workout.source}")
    print(f"Duration: {imported_workout.duration_minutes} minutes")
    
    
    print("\nRunning unit tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWorkoutApp)
    unittest.TextTestRunner(verbosity=1).run(suite)