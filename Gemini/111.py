import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict, Any, Optional, Protocol

class ActivityType(Enum):
    STRENGTH = auto()
    CARDIO = auto()
    HIIT = auto()
    FLEXIBILITY = auto()
    RECOVERY = auto()

@dataclass(frozen=True)
class PerformanceMetrics:
    heart_rate_avg: Optional[int] = None
    calories_burned: Optional[float] = None
    distance_km: Optional[float] = None
    duration_seconds: int = 0
    power_watts_avg: Optional[float] = None

@dataclass(frozen=True)
class ExerciseDetail:
    exercise_id: str
    name: str
    reps: Optional[int] = None
    sets: Optional[int] = None
    weight_kg: Optional[float] = None
    rpe: Optional[int] = None  

@dataclass
class WorkoutSession:
    session_id: str
    user_id: str
    start_time: datetime
    activity_type: ActivityType
    metrics: PerformanceMetrics
    exercises: List[ExerciseDetail] = field(default_factory=list)
    provider_source: str = "Internal"
    external_id: Optional[str] = None

class FitnessDataProvider(ABC):
    
    @abstractmethod
    def authenticate(self, auth_payload: Dict[str, str]) -> bool:
        pass

    @abstractmethod
    def fetch_recent_activities(self, since: datetime) -> List[WorkoutSession]:
        pass

class StravaAdapter(FitnessDataProvider):
    def authenticate(self, auth_payload: Dict[str, str]) -> bool:
        
        
        print(f"Establishing secure link to Strava for user: {auth_payload.get('user_id')}")
        return True

    def fetch_recent_activities(self, since: datetime) -> List[WorkoutSession]:
        
        return [
            WorkoutSession(
                session_id=str(uuid.uuid4()),
                user_id="amazon_user_8821",
                start_time=datetime.now(),
                activity_type=ActivityType.CARDIO,
                metrics=PerformanceMetrics(
                    heart_rate_avg=155, 
                    distance_km=10.5, 
                    duration_seconds=3600
                ),
                provider_source="Strava",
                external_id="strava_act_99283"
            )
        ]

class GarminConnectAdapter(FitnessDataProvider):
    def authenticate(self, auth_payload: Dict[str, str]) -> bool:
        print("Authenticating with Garmin Connect Cloud...")
        return True

    def fetch_recent_activities(self, since: datetime) -> List[WorkoutSession]:
        
        return [
            WorkoutSession(
                session_id=str(uuid.uuid4()),
                user_id="amazon_user_8821",
                start_time=datetime.now(),
                activity_type=ActivityType.STRENGTH,
                metrics=PerformanceMetrics(calories_burned=450, duration_seconds=2700),
                exercises=[
                    ExerciseDetail(exercise_id="ex_1", name="Deadlift", reps=5, sets=5, weight_kg=140.0),
                    ExerciseDetail(exercise_id="ex_2", name="Overhead Press", reps=8, sets=3, weight_kg=60.0)
                ],
                provider_source="Garmin",
                external_id="garmin_fit_0012"
            )
        ]

class IngestionService:
    
    def __init__(self):
        self._providers: Dict[str, FitnessDataProvider] = {}
        self._internal_repository: List[WorkoutSession] = []

    def register_provider(self, name: str, provider: FitnessDataProvider):
        self._providers[name.lower()] = provider

    def sync_external_data(self, user_id: str, provider_name: str, credentials: Dict[str, str]):
        provider = self._providers.get(provider_name.lower())
        if not provider:
            raise ValueError(f"Unsupported provider: {provider_name}")

        if provider.authenticate(credentials):
            
            
            incoming_workouts = provider.fetch_recent_activities(since=datetime.now())
            self._persist_workouts(incoming_workouts)
            return len(incoming_workouts)
        return 0

    def _persist_workouts(self, workouts: List[WorkoutSession]):
        
        for workout in workouts:
            print(f"Persisting {workout.activity_type.name} session from {workout.provider_source}")
            self._internal_repository.append(workout)

def main():
    
    app_service = IngestionService()
    
    
    app_service.register_provider("strava", StravaAdapter())
    app_service.register_provider("garmin", GarminConnectAdapter())

    
    user_context = {"user_id": "amazon_user_8821", "oauth_token": "v3_access_granted"}
    
    try:
        strava_count = app_service.sync_external_data("amazon_user_8821", "strava", user_context)
        garmin_count = app_service.sync_external_data("amazon_user_8821", "garmin", user_context)
        
        print(f"Synchronization complete. Total items imported: {strava_count + garmin_count}")
    except Exception as e:
        print(f"System error during ingestion: {e}")

if __name__ == "__main__":
    main()