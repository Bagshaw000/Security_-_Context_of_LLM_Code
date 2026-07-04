import abc
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import unittest

@dataclass
class Workout:
    
    workout_id: str
    source_app: str
    start_time: datetime
    duration_seconds: int
    activity_type: str
    distance_meters: Optional[float] = None
    calories_burned: Optional[float] = None

class FitnessDataImporter(abc.ABC):
    
    @abc.abstractmethod
    def import_data(self, credentials: Dict[str, str]) -> List[Workout]:
        pass

class StravaImporter(FitnessDataImporter):
    
    def import_data(self, credentials: Dict[str, str]) -> List[Workout]:
        
        
        
        return [
            Workout(
                workout_id="strava_run_101",
                source_app="Strava",
                start_time=datetime(2023, 11, 1, 7, 0, 0),
                duration_seconds=2400,
                activity_type="Run",
                distance_meters=5000.0,
                calories_burned=450.0
            )
        ]

class AppleHealthImporter(FitnessDataImporter):
    
    def import_data(self, credentials: Dict[str, str]) -> List[Workout]:
        
        return [
            Workout(
                workout_id="apple_health_992",
                source_app="Apple Health",
                start_time=datetime(2023, 11, 2, 18, 30, 0),
                duration_seconds=3600,
                activity_type="Yoga",
                calories_burned=200.0
            )
        ]

class WorkoutTrackerApp:
    
    def __init__(self):
        
        self.workouts: List[Workout] = []

    def add_workout(self, workout: Workout):
        
        if not any(w.workout_id == workout.workout_id for w in self.workouts):
            self.workouts.append(workout)

    def sync_external_data(self, importer: FitnessDataImporter, credentials: Dict[str, str]):
        
        try:
            new_workouts = importer.import_data(credentials)
            for workout in new_workouts:
                self.add_workout(workout)
        except Exception as e:
            print(f"Error syncing data: {e}")

    def get_weekly_stats(self) -> Dict[str, float]:
        
        total_seconds = sum(w.duration_seconds for w in self.workouts)
        total_calories = sum(w.calories_burned for w in self.workouts if w.calories_burned)
        return {
            "total_minutes": total_seconds / 60,
            "total_calories": total_calories,
            "workout_count": len(self.workouts)
        }

class TestWorkoutTracker(unittest.TestCase):
    
    def setUp(self):
        self.app = WorkoutTrackerApp()

    def test_add_workout(self):
        workout = Workout("test_1", "Manual", datetime.now(), 600, "Walk")
        self.app.add_workout(workout)
        self.assertEqual(len(self.app.workouts), 1)

    def test_duplicate_prevention(self):
        workout = Workout("unique_id", "Manual", datetime.now(), 600, "Walk")
        self.app.add_workout(workout)
        self.app.add_workout(workout)
        self.assertEqual(len(self.app.workouts), 1)

    def test_strava_sync(self):
        importer = StravaImporter()
        self.app.sync_external_data(importer, {"api_key": "mock_key"})
        self.assertEqual(self.app.workouts[0].source_app, "Strava")

if __name__ == "__main__":
    
    tracker = WorkoutTrackerApp()
    
    
    tracker.sync_external_data(StravaImporter(), {"token": "user_token_123"})
    tracker.sync_external_data(AppleHealthImporter(), {"file_path": "export.xml"})
    
    stats = tracker.get_weekly_stats()
    print(f"Sync complete. Total Workouts: {stats['workout_count']}")
    print(f"Total Active Minutes: {stats['total_minutes']:.2f}")

    
    print("\nRunning unit tests...")
    unittest.main(argv=[''], exit=False)
