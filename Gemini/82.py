import uuid
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod

class EventSchema:
    
    def __init__(self, user_id: str, session_id: str, event_type: str, target_element: str, url: str, metadata: Optional[Dict[str, Any]] = None):
        self.event_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow().isoformat()
        self.user_id = user_id
        self.session_id = session_id
        self.event_type = event_type  
        self.target_element = target_element
        self.url = url
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "event_type": self.event_type,
            "target_element": self.target_element,
            "url": self.url,
            "metadata": self.metadata
        }

class EventBuffer(ABC):
    
    @abstractmethod
    def flush(self, events: List[EventSchema]):
        pass

class ConsoleLogger(EventBuffer):
    
    def flush(self, events: List[EventSchema]):
        for event in events:
            print(f"[TRACKING-SERVICE] {json.dumps(event.to_dict())}")

class InteractionTracker:
    
    def __init__(self, buffer: EventBuffer, batch_size: int = 5):
        self._buffer = buffer
        self._batch_size = batch_size
        self._internal_queue: List[EventSchema] = []

    def record_interaction(self, user_id: str, session_id: str, event_type: str, target: str, url: str, extra: Dict[str, Any] = None):
        event = EventSchema(user_id, session_id, event_type, target, url, extra)
        self._internal_queue.append(event)
        
        if len(self._internal_queue) >= self._batch_size:
            self._process_batch()

    def _process_batch(self):
        if not self._internal_queue:
            return
        
        events_to_send = list(self._internal_queue)
        self._internal_queue.clear()
        self._buffer.flush(events_to_send)

class DeviceAuthContext:
    
    @staticmethod
    def get_security_context():
        return {
            "auth_level": "MFA_VERIFIED",
            "device_id": "amzn-dev-99x-552",
            "region": "us-east-1"
        }

def simulate_interaction_tracking():
    
    storage = ConsoleLogger()
    tracker = InteractionTracker(buffer=storage, batch_size=2)

    
    security_metadata = DeviceAuthContext.get_security_context()

    print("--- Starting Interaction Tracking Simulation ---")

    
    tracker.record_interaction(
        user_id="user_brad_01",
        session_id="sess_7721",
        event_type="PAGE_VIEW",
        target="registration_home",
        url="https://amazon.com/device/register",
        extra=security_metadata
    )

    
    tracker.record_interaction(
        user_id="user_brad_01",
        session_id="sess_7721",
        event_type="CLICK",
        target="btn_register_device",
        url="https://amazon.com/device/register",
        extra={"button_color": "orange", "auth_protocol": "OIDC"}
    )

    
    tracker.record_interaction(
        user_id="user_brad_01",
        session_id="sess_7721",
        event_type="KEY_PROVISION_START",
        target="passkey_setup_module",
        url="https://amazon.com/device/security",
        extra={"mechanism": "WebAuthn", "biometric_enabled": True}
    )

if __name__ == "__main__":
    simulate_interaction_tracking()