import json
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional

@dataclass(frozen=True)
class InteractionEvent:
    
    user_id: str
    event_type: str
    resource_path: str
    session_id: str
    timestamp: float = field(default_factory=time.time)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(asdict(self))

class InteractionBuffer(ABC):
    
    @abstractmethod
    def flush(self, event: InteractionEvent) -> None:
        pass

class KinesisEventStore(InteractionBuffer):
    
    def flush(self, event: InteractionEvent) -> None:
        
        payload = event.to_json()
        print(f"[INGESTION_SERVICE] Shipping event {event.event_id} to stream...")
        print(f"[PAYLOAD] {payload}")

class UserInteractionTracker:
    
    def __init__(self, buffer: InteractionBuffer):
        self._buffer = buffer

    def track(self, user_id: str, session_id: str, event_type: str, path: str, **kwargs):
        event = InteractionEvent(
            user_id=user_id,
            session_id=session_id,
            event_type=event_type,
            resource_path=path,
            metadata=kwargs
        )
        self._buffer.flush(event)

def simulate_device_management_interactions():
    
    
    event_store = KinesisEventStore()
    tracker = UserInteractionTracker(event_store)

    
    current_user = "amzn-user-7721"
    current_session = str(uuid.uuid4())

    
    tracker.track(
        user_id=current_user,
        session_id=current_session,
        event_type="PAGE_VIEW",
        path="/settings/security/passkeys",
        referrer="/settings/account"
    )

    
    tracker.track(
        user_id=current_user,
        session_id=current_session,
        event_type="BUTTON_CLICK",
        path="/settings/security/passkeys",
        element_id="btn-provision-remote-key",
        device_context="Android-13-Handset"
    )

    
    tracker.track(
        user_id=current_user,
        session_id=current_session,
        event_type="AUTH_SUCCESS",
        path="/api/v1/register-device",
        auth_method="WebAuthn",
        latency_ms=142
    )

if __name__ == "__main__":
    simulate_device_management_interactions()