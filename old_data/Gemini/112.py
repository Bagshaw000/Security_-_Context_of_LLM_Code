import abc
import uuid
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum, auto
from dataclasses import dataclass, field

class ActivityType(Enum):
    RUNNING = auto()
    CYCLING = auto()
    STRENGTH_TRAINING = auto()
    SWIMMING = auto()
    HIIT = auto()

@dataclass(frozen=True)
class ExerciseMetric:
    
    name: str
    value: float
    unit: str

@dataclass
class WorkoutRecord:
    
    workout_id: str
    user_id: str
    activity_type: ActivityType
    start_time: datetime
    end_time: Optional[datetime]
    metrics: List[ExerciseMetric]
    provider_id: str
    external_sync_id: str
    ingestion_timestamp: datetime = field(default_factory=datetime.utcnow)

class FitnessDataImporter(abc.ABC):
    
    
    @abc.abstractmethod
    def authorize(self, auth_payload: Dict[str, str]) -> bool:
        
        pass

    @abc.abstractmethod
    def fetch_workouts(self, user_id: str, since: datetime) -> List[WorkoutRecord]:
        
        pass

class StravaImporter(FitnessDataImporter):
    def authorize(self, auth_payload: Dict[str, str]) -> bool:
        
        return "access_token" in auth_payload

    def fetch_workouts(self, user_id: str, since: datetime) -> List[WorkoutRecord]:
        
        mock_raw_data = [
            {
                "id": "strava_act_987",
                "type": "Run",
                "start_date": "2023-11-15T08:30:00Z",
                "distance": 5000.0,
                "elapsed_time": 1500
            }
        ]
        
        normalized_records = []
        for item in mock_raw_data:
            record = WorkoutRecord(
                workout_id=str(uuid.uuid4()),
                user_id=user_id,
                activity_type=ActivityType.RUNNING,
                start_time=datetime.fromisoformat(item["start_date"].replace("Z", "+00:00")),
                end_time=None,
                metrics=[
                    ExerciseMetric("distance", item["distance"], "meters"),
                    ExerciseMetric("duration", item["elapsed_time"], "seconds")
                ],
                provider_id="STRAVA_V3",
                external_sync_id=item["id"]
            )
            normalized_records.append(record)
        return normalized_records

class AppleHealthImporter(FitnessDataImporter):
    def authorize(self, auth_payload: Dict[str, str]) -> bool:
        
        return True

    def fetch_workouts(self, user_id: str, since: datetime) -> List[WorkoutRecord]:
        
        mock_raw_data = [
            {
                "uuid": "apple_uid_111",
                "workoutType": "HKWorkoutActivityTypeCycling",
                "startDate": "2023-11-16T17:00:00Z",
                "energyBurned": 450.5
            }
        ]
        
        normalized_records = []
        for item in mock_raw_data:
            record = WorkoutRecord(
                workout_id=str(uuid.uuid4()),
                user_id=user_id,
                activity_type=ActivityType.CYCLING,
                start_time=datetime.fromisoformat(item["startDate"].replace("Z", "+00:00")),
                end_time=None,
                metrics=[ExerciseMetric("active_calories", item["energyBurned"], "kcal")],
                provider_id="APPLE_HEALTH_KIT",
                external_sync_id=item["uuid"]
            )
            normalized_records.append(record)
        return normalized_records

class IdentityLinkingManager:
    
    def __init__(self):
        
        self._identity_map: Dict[str, Dict[str, Dict[str, str]]] = {}

    def link_account(self, internal_user_id: str, provider_id: str, secrets: Dict[str, str]):
        
        if internal_user_id not in self._identity_map:
            self._identity_map[internal_user_id] = {}
        
        self._identity_map[internal_user_id][provider_id] = secrets

    def get_provider_credentials(self, internal_user_id: str, provider_id: str) -> Optional[Dict[str, str]]:
        return self._identity_map.get(internal_user_id, {}).get(provider_id)

class WorkoutTrackingService:
    
    def __init__(self, identity_manager: IdentityLinkingManager):
        self.identity_manager = identity_manager
        self.importers: Dict[str, FitnessDataImporter] = {
            "STRAVA": StravaImporter(),
            "APPLE_HEALTH": AppleHealthImporter()
        }
        self.repository: List[WorkoutRecord] = []

    def synchronize_all_providers(self, user_id: str):
        
        for provider_name, importer in self.importers.items():
            creds = self.identity_manager.get_provider_credentials(user_id, provider_name)
            if creds and importer.authorize(creds):
                new_data = importer.fetch_workouts(user_id, since=datetime.min)
                self._upsert_workouts(new_data)

    def _upsert_workouts(self, records: List[WorkoutRecord]):
        
        for record in records:
            
            exists = any(r.external_sync_id == record.external_sync_id for r in self.repository)
            if not exists:
                self.repository.append(record)
                print(f"Ingested {record.activity_type.name} from {record.provider_id}")

if __name__ == "__main__":
    
    id_manager = IdentityLinkingManager()
    app_service = WorkoutTrackingService(id_manager)

    
    current_user = "amzn-user-uuid-001"
    id_manager.link_account(current_user, "STRAVA", {"access_token": "v3_oauth_token_xyz"})
    id_manager.link_account(current_user, "APPLE_HEALTH", {"session": "healthkit_active"})

    
    print(f"Starting sync for user: {current_user}...")
    app_service.synchronize_all_providers(current_user)

    
    print(f"Total workouts tracked: {len(app_service.repository)}")
    for workout in app_service.repository:
        print(f" - {workout.start_time}: {workout.activity_type.name} ({workout.provider_id})")