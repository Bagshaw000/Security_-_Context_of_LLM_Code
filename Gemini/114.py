import abc
import uuid
import logging
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FitnessIngestionService")

@dataclass(frozen=True)
class Exercise:
    
    name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight_kg: Optional[float] = None
    duration_seconds: Optional[int] = None
    distance_meters: Optional[float] = None

@dataclass(frozen=True)
class Workout:
    
    workout_id: str
    external_id: str
    user_id: str
    provider_name: str
    timestamp: datetime
    exercises: List[Exercise]
    metadata: Dict[str, Any] = field(default_factory=dict)

class FitnessProviderPlugin(abc.ABC):
    
    @abc.abstractmethod
    def fetch_workouts(self, access_token: str, last_sync: datetime) -> List[Workout]:
        pass

class StravaProvider(FitnessProviderPlugin):
    
    def fetch_workouts(self, access_token: str, last_sync: datetime) -> List[Workout]:
        
        logger.info("Polling Strava activity stream...")
        return [
            Workout(
                workout_id=str(uuid.uuid4()),
                external_id="strava_act_5521",
                user_id="u_99",
                provider_name="Strava",
                timestamp=datetime.utcnow(),
                exercises=[Exercise(name="Cycling", distance_meters=25000.0, duration_seconds=3600)]
            )
        ]

class AppleHealthProvider(FitnessProviderPlugin):
    
    def fetch_workouts(self, access_token: str, last_sync: datetime) -> List[Workout]:
        logger.info("Processing HealthKit XML/JSON payload...")
        return []

class FitbitProvider(FitnessProviderPlugin):
    
    def fetch_workouts(self, access_token: str, last_sync: datetime) -> List[Workout]:
        logger.info("Querying Fitbit intraday time-series data...")
        return []

class AccountLinkingManager:
    
    def __init__(self):
        self._token_store: Dict[str, Dict[str, str]] = {}

    def link_external_account(self, user_id: str, provider: str, oauth_token: str):
        if user_id not in self._token_store:
            self._token_store[user_id] = {}
        self._token_store[user_id][provider.lower()] = oauth_token
        logger.info(f"Successfully linked {provider} for user {user_id}")

    def get_credentials(self, user_id: str, provider: str) -> Optional[str]:
        return self._token_store.get(user_id, {}).get(provider.lower())

class WorkoutIngestionEngine:
    
    def __init__(self, auth_manager: AccountLinkingManager):
        self.auth_manager = auth_manager
        self._providers: Dict[str, FitnessProviderPlugin] = {}
        self._persistence_layer: List[Workout] = []

    def register_provider(self, name: str, provider: FitnessProviderPlugin):
        self._providers[name.lower()] = provider

    def sync_all_sources(self, user_id: str):
        
        for name, plugin in self._providers.items():
            token = self.auth_manager.get_credentials(user_id, name)
            if not token:
                continue
            
            try:
                
                new_data = plugin.fetch_workouts(token, datetime.min)
                self._persistence_layer.extend(new_data)
                logger.info(f"Ingested {len(new_data)} records from {name}")
            except Exception as e:
                logger.error(f"Ingestion failure for {name}: {str(e)}")

def bootstrap_application():
    
    
    auth_service = AccountLinkingManager()
    ingestion_engine = WorkoutIngestionEngine(auth_service)

    
    ingestion_engine.register_provider("strava", StravaProvider())
    ingestion_engine.register_provider("apple_health", AppleHealthProvider())
    ingestion_engine.register_provider("fitbit", FitbitProvider())

    
    current_user = "brad_amazon_dev"
    auth_service.link_external_account(current_user, "strava", "access_token_abc_123")

    
    ingestion_engine.sync_all_sources(current_user)

if __name__ == "__main__":
    bootstrap_application()