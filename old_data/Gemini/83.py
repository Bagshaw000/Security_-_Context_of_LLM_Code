import uuid
import time
import json
import threading
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, field
from enum import Enum, auto
from abc import ABC, abstractmethod

class InteractionType(Enum):
    PAGE_VIEW = auto()
    CLICK = auto()
    FORM_SUBMIT = auto()
    AUTH_CHALLENGE = auto()
    PASSKEY_REGISTRATION = auto()
    ACCOUNT_LINK_INITIATED = auto()
    SESSION_START = auto()

@dataclass
class InteractionEvent:
    
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    event_type: InteractionType = InteractionType.PAGE_VIEW
    timestamp: float = field(default_factory=time.time)
    schema_version: str = "1.0.4"
    payload: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)

    def serialize(self) -> str:
        
        data = asdict(self)
        data['event_type'] = self.event_type.name
        data['timestamp_iso'] = datetime.fromtimestamp(self.timestamp).isoformat()
        return json.dumps(data)

class EventSink(ABC):
    
    @abstractmethod
    def emit(self, event: InteractionEvent) -> None:
        pass

class HighScaleLogSink(EventSink):
    
    def emit(self, event: InteractionEvent) -> None:
        
        payload = event.serialize()
        
        print(f"[LOG-SINK] {event.event_type.name} | {event.event_id} | Payload Size: {len(payload)} bytes")

class InteractionTracker:
    
    def __init__(self, sink: EventSink):
        self._sink = sink
        self._lock = threading.Lock()

    def log_interaction(self, 
                       user_id: str, 
                       session_id: str, 
                       event_type: InteractionType, 
                       payload: Dict[str, Any],
                       context: Optional[Dict[str, Any]] = None) -> str:
        
        event = InteractionEvent(
            user_id=user_id,
            session_id=session_id,
            event_type=event_type,
            payload=payload,
            context=context or {}
        )
        
        
        with self._lock:
            self._sink.emit(event)
        
        return event.event_id

class DeviceAuthTelemetryManager:
    
    def __init__(self, tracker: InteractionTracker):
        self._tracker = tracker

    def track_passkey_provisioning(self, user_id: str, session_id: str, device_id: str, status: str):
        self._tracker.log_interaction(
            user_id=user_id,
            session_id=session_id,
            event_type=InteractionType.PASSKEY_REGISTRATION,
            payload={
                "device_id": device_id, 
                "provisioning_status": status,
                "auth_method": "webauthn_rs256"
            },
            context={"service": "RemoteKeyProvisioning", "region": "us-east-1"}
        )

    def track_account_linking(self, user_id: str, session_id: str, partner_id: str):
        self._tracker.log_interaction(
            user_id=user_id,
            session_id=session_id,
            event_type=InteractionType.ACCOUNT_LINK_INITIATED,
            payload={"partner": partner_id},
            context={"service": "AccountLinkingService"}
        )


if __name__ == "__main__":
    
    sink = HighScaleLogSink()
    main_tracker = InteractionTracker(sink)
    auth_telemetry = DeviceAuthTelemetryManager(main_tracker)

    
    current_user = "amzn-user-99021-x"
    current_session = str(uuid.uuid4())

    
    main_tracker.log_interaction(
        user_id=current_user,
        session_id=current_session,
        event_type=InteractionType.PAGE_VIEW,
        payload={"url": "/settings/security/passkeys", "entry_point": "dashboard"},
        context={"ua": "Mozilla/5.0", "ip_obfuscated": "192.168.x.x"}
    )

    
    auth_telemetry.track_passkey_provisioning(
        user_id=current_user,
        session_id=current_session,
        device_id="fire-tablet-gen12",
        status="SUCCESS"
    )

    
    main_tracker.log_interaction(
        user_id=current_user,
        session_id=current_session,
        event_type=InteractionType.CLICK,
        payload={"element_id": "learn-more-passkeys-link"},
        context={"viewport_size": "1080x1920"}
    )

    
    auth_telemetry.track_account_linking(
        user_id=current_user,
        session_id=current_session,
        partner_id="prime-video-external-auth"
    )