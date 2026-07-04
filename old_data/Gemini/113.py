import abc
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict, Optional, Protocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkoutType(Enum):
    STRENGTH = auto()
    CARDIO = auto()
    HIIT = auto()
    FLEXIBILITY = auto()

@dataclass(frozen=True)
class ExerciseSet:
    weight_kg: float
    reps: int
    rpe: Optional[float] = None
    rest_seconds: int = 60

@dataclass
class Exercise:
    name: str
    sets: List[ExerciseSet] = field(default_factory=list)
    notes: Optional[str] = None

@dataclass
class WorkoutSession:
    workout_id: str
    user_id: str
    start_time: datetime
    end_time: datetime
    workout_type: WorkoutType
    exercises: List[Exercise] = field(default_factory=list)
    source_provider: str = "Native"

class FitnessDataImporter(abc.ABC):
    
    @abc.abstractmethod
    def transform_to_internal_format(self, raw_data: str) -> List[WorkoutSession]:
        pass

class StravaImporter(FitnessDataImporter):
    
    def transform_to_internal_format(self, raw_data: str) -> List[WorkoutSession]:
        
        data = json.loads(raw_data)
        sessions = []
        for activity in data:
            session = WorkoutSession(
                workout_id=str(uuid.uuid4()),
                user_id=activity.get("athlete_id"),
                start_time=datetime.fromisoformat(activity["start_date"]),
                end_time=datetime.fromisoformat(activity["end_date"]),
                workout_type=WorkoutType.CARDIO,
                source_provider="Strava"
            )
            sessions.append(session)
        return sessions

class AppleHealthImporter(FitnessDataImporter):
    
    def transform_to_internal_format(self, raw_data: str) -> List[WorkoutSession]:
        
        data = json.loads(raw_data)
        sessions = []
        for record in data:
            session = WorkoutSession(
                workout_id=str(uuid.uuid4()),
                user_id="local_user",
                start_time=datetime.fromisoformat(record["startDate"]),
                end_time=datetime.fromisoformat(record["endDate"]),
                workout_type=WorkoutType.STRENGTH,
                source_provider="AppleHealth"
            )
            sessions.append(session)
        return sessions

class WorkoutTrackerService:
    
    def __init__(self):
        self._storage: Dict[str, WorkoutSession] = {}
        self._importers: Dict[str, FitnessDataImporter] = {
            "strava": StravaImporter(),
            "apple_health": AppleHealthImporter()
        }

    def import_external_data(self, provider_name: str, payload: str) -> int:
        
        importer = self._importers.get(provider_name.lower())
        if not importer:
            raise ValueError(f"Provider {provider_name} is not supported.")

        try:
            sessions = importer.transform_to_internal_format(payload)
            for session in sessions:
                self._storage[session.workout_id] = session
            
            logger.info(f"Successfully imported {len(sessions)} sessions from {provider_name}.")
            return len(sessions)
        except Exception as e:
            logger.error(f"Failed to import data from {provider_name}: {str(e)}")
            raise

    def get_user_workouts(self, user_id: str) -> List[WorkoutSession]:
        return [s for s in self._storage.values() if s.user_id == user_id]

def run_demonstration():
    
    strava_json_payload = json.dumps([
        {
            "athlete_id": "user_123",
            "start_date": "2023-10-27T08:00:00",
            "end_date": "2023-10-27T09:00:00",
            "type": "Run"
        }
    ])

    
    tracker = WorkoutTrackerService()

    
    tracker.import_external_data("strava", strava_json_payload)

    
    workouts = tracker.get_user_workouts("user_123")
    for w in workouts:
        print(f"Workout Found: ID={w.workout_id}, Provider={w.source_provider}, Start={w.start_time}")

if __name__ == "__main__":
    run_demonstration()