import abc
import uuid
import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum, auto
from typing import List, Dict, Optional, Any, Protocol


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkoutType(Enum):
    RUN = auto()
    STRENGTH = auto()
    CYCLING = auto()
    HIIT = auto()
    YOGA = auto()

@dataclass(frozen=True)
class Exercise:
    name: str
    sets: int
    reps: Optional[int] = None
    weight_kg: Optional[float] = None
    duration_seconds: Optional[int] = None

@dataclass(frozen=True)
class WorkoutSession:
    session_id: uuid.UUID
    user_id: str
    workout_type: WorkoutType
    start_time: datetime
    end_time: datetime
    exercises: List[Exercise]
    source_provider: str
    external_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class ExternalFitnessProvider(abc.ABC):
    
    @abc.abstractmethod
    def get_provider_name(self) -> str:
        pass

    @abc.abstractmethod
    def fetch_raw_data(self, external_user_id: str, last_sync: datetime) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def normalize(self, raw_data: Dict[str, Any], internal_user_id: str) -> WorkoutSession:
        pass

class StravaProvider(ExternalFitnessProvider):
    def get_provider_name(self) -> str:
        return "STRAVA"

    def fetch_raw_data(self, external_user_id: str, last_sync: datetime) -> List[Dict[str, Any]]:
        
        logger.info(f"Fetching data from Strava for user {external_user_id}")
        return [{"id": "st_123", "type": "Run", "start_date": "2023-10-27T08:00:00Z", "elapsed_time": 1800}]

    def normalize(self, raw_data: Dict[str, Any], internal_user_id: str) -> WorkoutSession:
        
        return WorkoutSession(
            session_id=uuid.uuid4(),
            user_id=internal_user_id,
            workout_type=WorkoutType.RUN,
            start_time=datetime.fromisoformat(raw_data["start_date"].replace("Z", "+00:00")),
            end_time=datetime.now(), 
            exercises=[],
            source_provider=self.get_provider_name(),
            external_id=raw_data["id"]
        )

class GarminProvider(ExternalFitnessProvider):
    def get_provider_name(self) -> str:
        return "GARMIN"

    def fetch_raw_data(self, external_user_id: str, last_sync: datetime) -> List[Dict[str, Any]]:
        logger.info(f"Fetching data from Garmin Connect for user {external_user_id}")
        return [{"activityId": "gm_999", "activityType": "STRENGTH_TRAINING", "startTime": 1698403200}]

    def normalize(self, raw_data: Dict[str, Any], internal_user_id: str) -> WorkoutSession:
        return WorkoutSession(
            session_id=uuid.uuid4(),
            user_id=internal_user_id,
            workout_type=WorkoutType.STRENGTH,
            start_time=datetime.fromtimestamp(raw_data["startTime"]),
            end_time=datetime.now(),
            exercises=[],
            source_provider=self.get_provider_name(),
            external_id=raw_data["activityId"]
        )

class AccountLinkingService:
    
    def __init__(self):
        
        self._registry: Dict[str, Dict[str, str]] = {}

    def link_account(self, internal_user_id: str, provider_name: str, external_user_id: str):
        if internal_user_id not in self._registry:
            self._registry[internal_user_id] = {}
        self._registry[internal_user_id][provider_name] = external_user_id
        logger.info(f"Linked {provider_name} account {external_user_id} to user {internal_user_id}")

    def get_external_id(self, internal_user_id: str, provider_name: str) -> Optional[str]:
        return self._registry.get(internal_user_id, {}).get(provider_name)

class WorkoutIngestionEngine:
    
    def __init__(self, account_service: AccountLinkingService):
        self.account_service = account_service
        self.providers: Dict[str, ExternalFitnessProvider] = {}

    def register_provider(self, provider: ExternalFitnessProvider):
        self.providers[provider.get_provider_name()] = provider

    def sync_user_data(self, internal_user_id: str, last_sync: datetime) -> List[WorkoutSession]:
        synced_sessions = []
        
        for provider_name, provider in self.providers.items():
            external_id = self.account_service.get_external_id(internal_user_id, provider_name)
            if not external_id:
                continue
            
            try:
                raw_activities = provider.fetch_raw_data(external_id, last_sync)
                for activity in raw_activities:
                    normalized_session = provider.normalize(activity, internal_user_id)
                    synced_sessions.append(normalized_session)
                    
                    self._persist_session(normalized_session)
            except Exception as e:
                logger.error(f"Failed to sync from {provider_name} for user {internal_user_id}: {str(e)}")
        
        return synced_sessions

    def _persist_session(self, session: WorkoutSession):
        
        logger.info(f"Persisting session {session.session_id} from {session.source_provider}")


if __name__ == "__main__":
    
    linking_service = AccountLinkingService()
    ingestion_engine = WorkoutIngestionEngine(linking_service)

    
    ingestion_engine.register_provider(StravaProvider())
    ingestion_engine.register_provider(GarminProvider())

    
    USER_ID = "amazon_internal_user_7788"
    linking_service.link_account(USER_ID, "STRAVA", "strava_athlete_456")
    linking_service.link_account(USER_ID, "GARMIN", "garmin_user_001")

    
    last_sync_time = datetime(2023, 1, 1)
    results = ingestion_engine.sync_user_data(USER_ID, last_sync_time)

    print(f"Successfully synced {len(results)} workout sessions.")
    for res in results:
        print(f" - Provider: {res.source_provider}, Type: {res.workout_type.name}, ID: {res.external_id}")