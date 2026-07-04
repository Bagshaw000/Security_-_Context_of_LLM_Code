import abc
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
import unittest
import json

@dataclass
class Exercise:
    name: str
    sets: int
    reps: int
    weight_kg: float

@dataclass
class Workout:
    workout_id: str
    user_id: str
    timestamp: datetime
    exercises: List[Exercise]
    source_app: str

class FitnessDataImporter(abc.ABC):
    
    @abc.abstractmethod
    def fetch_data(self, external_user_id: str) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Workout]:
        pass

class StravaImporter(FitnessDataImporter):
    def fetch_data(self, external_user_id: str) -> List[Dict[str, Any]]:
        
        return [
            {
                "id": "strava_act_98765",
                "start_date": "2023-11-01T08:00:00Z",
                "type": "WeightTraining",
                "exercises": [
                    {"name": "Deadlift", "sets": 3, "reps": 5, "weight": 100.0},
                    {"name": "Overhead Press", "sets": 3, "reps": 8, "weight": 40.0}
                ]
            }
        ]

    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Workout]:
        workouts = []
        for item in raw_data:
            exercises = [
                Exercise(
                    name=ex["name"], 
                    sets=ex["sets"], 
                    reps=ex["reps"], 
                    weight_kg=ex["weight"]
                ) for ex in item.get("exercises", [])
            ]
            workouts.append(Workout(
                workout_id=item["id"],
                user_id="local_user_001",
                timestamp=datetime.fromisoformat(item["start_date"].replace("Z", "+00:00")),
                exercises=exercises,
                source_app="Strava"
            ))
        return workouts

class GarminImporter(FitnessDataImporter):
    def fetch_data(self, external_user_id: str) -> List[Dict[str, Any]]:
        
        return [
            {
                "activityId": "garmin_raw_1122",
                "startTimeLocal": "2023-11-02T17:30:00",
                "activityType": "STRENGTH_TRAINING",
                "laps": [
                    {"exerciseName": "Bench Press", "repetitionCount": 10, "weight": 60.0},
                    {"exerciseName": "Bench Press", "repetitionCount": 10, "weight": 60.0}
                ]
            }
        ]

    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Workout]:
        workouts = []
        for item in raw_data:
            
            exercise_map = {}
            for lap in item.get("laps", []):
                name = lap["exerciseName"]
                if name not in exercise_map:
                    exercise_map[name] = {"sets": 0, "reps": 0, "weight": lap["weight"]}
                exercise_map[name]["sets"] += 1
                exercise_map[name]["reps"] = lap["repetitionCount"] 

            exercises = [
                Exercise(name=k, sets=v["sets"], reps=v["reps"], weight_kg=v["weight"])
                for k, v in exercise_map.items()
            ]
            
            workouts.append(Workout(
                workout_id=item["activityId"],
                user_id="local_user_001",
                timestamp=datetime.fromisoformat(item["startTimeLocal"]),
                exercises=exercises,
                source_app="Garmin"
            ))
        return workouts

class WorkoutTrackerService:
    
    def __init__(self):
        self._storage: Dict[str, Workout] = {}

    def import_external_data(self, importer: FitnessDataImporter, external_id: str):
        raw_data = importer.fetch_data(external_id)
        transformed_workouts = importer.transform(raw_data)
        for workout in transformed_workouts:
            self.save_workout(workout)
        return len(transformed_workouts)

    def save_workout(self, workout: Workout):
        
        self._storage[workout.workout_id] = workout

    def get_user_history(self) -> List[Workout]:
        return sorted(self._storage.values(), key=lambda x: x.timestamp, reverse=True)

class TestWorkoutApp(unittest.TestCase):
    
    def setUp(self):
        self.service = WorkoutTrackerService()

    def test_strava_import_flow(self):
        importer = StravaImporter()
        count = self.service.import_external_data(importer, "strava_user_johndoe")
        
        self.assertEqual(count, 1)
        history = self.service.get_user_history()
        self.assertEqual(history[0].source_app, "Strava")
        self.assertEqual(history[0].exercises[0].name, "Deadlift")

    def test_garmin_import_flow(self):
        importer = GarminImporter()
        self.service.import_external_data(importer, "garmin_user_johndoe")
        
        history = self.service.get_user_history()
        garmin_workout = next(w for w in history if w.source_app == "Garmin")
        self.assertEqual(garmin_workout.exercises[0].name, "Bench Press")
        self.assertEqual(garmin_workout.exercises[0].sets, 2)

if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWorkoutApp)
    unittest.TextTestRunner(verbosity=2).run(suite)

    
    tracker = WorkoutTrackerService()
    strava = StravaImporter()
    garmin = GarminImporter()

    tracker.import_external_data(strava, "user_id_1")
    tracker.import_external_data(garmin, "user_id_1")

    print(f"\nTotal workouts tracked: {len(tracker.get_user_history())}")
    for workout in tracker.get_user_history():
        print(f"Date: {workout.timestamp} | Source: {workout.source_app} | Exercises: {len(workout.exercises)}")