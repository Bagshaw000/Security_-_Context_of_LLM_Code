import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict, Optional, Any


class ActivityType(Enum):
    RUNNING = auto()
    CYCLING = auto()
    WEIGHTLIFTING = auto()
    SWIMMING = auto()
    HIIT = auto()


@dataclass(frozen=True)
class ExerciseMetric:
    name: str
    value: float
    unit: str


@dataclass
class Exercise:
    name: str
    sets: int
    reps: Optional[int] = None
    weight: Optional[float] = None
    duration_seconds: Optional[int] = None
    metrics: List[ExerciseMetric] = field(default_factory=list)


@dataclass
class WorkoutSession:
    session_id: str
    user_id: str
    start_time: datetime
    end_time: datetime
    activity_type: ActivityType
    exercises: List[Exercise]
    source_app: str
    external_id: Optional[str] = None

    def get_duration_minutes(self) -> float:
        return (self.end_time - self.start_time).total_seconds() / 60.0


class DataImporter(ABC):
    
    
    @abstractmethod
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        pass

    @abstractmethod
    def fetch_raw_data(self, start_date: datetime) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def transform(self, raw_data: Dict[str, Any], user_id: str) -> WorkoutSession:
        pass


class StravaImporter(DataImporter):
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        
        print(f"Authenticating with Strava using client_id: {credentials.get('client_id')}")
        return True

    def fetch_raw_data(self, start_date: datetime) -> List[Dict[str, Any]]:
        
        return [
            {
                "id": "strava_12345",
                "type": "Run",
                "start_date": "2023-10-27T08:00:00Z",
                "elapsed_time": 3600,
                "distance": 10000,
                "average_heartrate": 155
            }
        ]

    def transform(self, raw_data: Dict[str, Any], user_id: str) -> WorkoutSession:
        start_time = datetime.fromisoformat(raw_data["start_date"].replace("Z", "+00:00"))
        end_time = datetime.fromtimestamp(start_time.timestamp() + raw_data["elapsed_time"])
        
        run_exercise = Exercise(
            name="Outdoor Run",
            sets=1,
            duration_seconds=raw_data["elapsed_time"],
            metrics=[
                ExerciseMetric("distance", raw_data["distance"], "meters"),
                ExerciseMetric("heart_rate", raw_data["average_heartrate"], "bpm")
            ]
        )

        return WorkoutSession(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            activity_type=ActivityType.RUNNING,
            exercises=[run_exercise],
            source_app="Strava",
            external_id=raw_data["id"]
        )


class AppleHealthImporter(DataImporter):
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        
        return True

    def fetch_raw_data(self, start_date: datetime) -> List[Dict[str, Any]]:
        
        return [
            {
                "uuid": "apple_67890",
                "workoutType": "HKWorkoutActivityTypeFunctionalStrengthTraining",
                "startDate": "2023-10-27T17:00:00Z",
                "endDate": "2023-10-27T18:00:00Z",
                "energyBurned": 450
            }
        ]

    def transform(self, raw_data: Dict[str, Any], user_id: str) -> WorkoutSession:
        start_time = datetime.fromisoformat(raw_data["startDate"].replace("Z", "+00:00"))
        end_time = datetime.fromisoformat(raw_data["endDate"].replace("Z", "+00:00"))
        
        strength_exercise = Exercise(
            name="Strength Training",
            sets=1,
            metrics=[ExerciseMetric("active_calories", raw_data["energyBurned"], "kcal")]
        )

        return WorkoutSession(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            activity_type=ActivityType.WEIGHTLIFTING,
            exercises=[strength_exercise],
            source_app="AppleHealth",
            external_id=raw_data["uuid"]
        )


class AccountLinker:
    
    
    def __init__(self):
        self._registry: Dict[str, Dict[str, str]] = {}

    def link_account(self, user_id: str, provider: str, external_token: str):
        if user_id not in self._registry:
            self._registry[user_id] = {}
        self._registry[user_id][provider] = external_token
        print(f"Successfully linked {provider} for user {user_id}")

    def get_token(self, user_id: str, provider: str) -> Optional[str]:
        return self._registry.get(user_id, {}).get(provider)


class WorkoutTrackingService:
    
    
    def __init__(self, account_linker: AccountLinker):
        self.account_linker = account_linker
        self.importers: Dict[str, DataImporter] = {
            "strava": StravaImporter(),
            "apple_health": AppleHealthImporter()
        }
        self.db: List[WorkoutSession] = []

    def sync_external_data(self, user_id: str, provider_name: str):
        importer = self.importers.get(provider_name)
        if not importer:
            raise ValueError(f"Unsupported provider: {provider_name}")

        token = self.account_linker.get_token(user_id, provider_name)
        if not token:
            raise PermissionError(f"User {user_id} has not linked {provider_name}")

        
        raw_activities = importer.fetch_raw_data(start_date=datetime.now())
        
        for raw_item in raw_activities:
            workout = importer.transform(raw_item, user_id)
            self._persist_workout(workout)

    def _persist_workout(self, workout: WorkoutSession):
        
        if any(w.external_id == workout.external_id for w in self.db if w.external_id):
            print(f"Workout {workout.external_id} already exists. Skipping.")
            return
        
        self.db.append(workout)
        print(f"Saved workout {workout.session_id} from {workout.source_app}")

    def get_user_stats(self, user_id: str):
        user_workouts = [w for w in self.db if w.user_id == user_id]
        total_minutes = sum(w.get_duration_minutes() for w in user_workouts)
        return {
            "count": len(user_workouts),
            "total_minutes": total_minutes,
            "activities": [w.activity_type.name for w in user_workouts]
        }


def main():
    
    linker = AccountLinker()
    service = WorkoutTrackingService(linker)
    
    current_user_id = "amazon_user_99"
    
    
    linker.link_account(current_user_id, "strava", "oauth_token_abc_123")
    linker.link_account(current_user_id, "apple_health", "system_permission_granted")
    
    
    print("--- Starting Sync ---")
    service.sync_external_data(current_user_id, "strava")
    service.sync_external_data(current_user_id, "apple_health")
    
    
    stats = service.get_user_stats(current_user_id)
    print("--- User Stats ---")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()