import time
import uuid
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("InteractionTrackingService")

@dataclass(frozen=True)
class InteractionEvent:
    
    event_id: str
    user_id: str
    session_id: str
    event_type: str  
    schema_version: str
    timestamp: datetime
    page_url: str
    user_agent: str
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return json.dumps(data)

class EventSink(ABC):
    
    @abstractmethod
    def emit(self, event: InteractionEvent) -> bool:
        pass

class KinesisEventSink(EventSink):
    
    def __init__(self, stream_name: str, region: str = "us-east-1"):
        self.stream_name = stream_name
        self.region = region

    def emit(self, event: InteractionEvent) -> bool:
        
        payload = event.to_json()
        logger.info(f"Emitting event {event.event_id} to stream {self.stream_name} [PartitionKey: {event.user_id}]")
        return True

class SessionContext:
    
    def __init__(self):
        self._sessions: Dict[str, str] = {}

    def get_session_id(self, user_id: str) -> str:
        if user_id not in self._sessions:
            self._sessions[user_id] = str(uuid.uuid1())
        return self._sessions[user_id]

    def rotate_session(self, user_id: str) -> None:
        self._sessions[user_id] = str(uuid.uuid1())

class InteractionTracker:
    
    def __init__(self, sink: EventSink, session_manager: SessionContext):
        self.sink = sink
        self.session_manager = session_manager
        self.version = "1.0.0"

    def capture(self, 
                user_id: str, 
                event_type: str, 
                page_url: str, 
                user_agent: str, 
                metadata: Optional[Dict] = None) -> Optional[str]:
        try:
            session_id = self.session_manager.get_session_id(user_id)
            
            event = InteractionEvent(
                event_id=str(uuid.uuid4()),
                user_id=user_id,
                session_id=session_id,
                event_type=event_type,
                schema_version=self.version,
                timestamp=datetime.now(timezone.utc),
                page_url=page_url,
                user_agent=user_agent,
                payload=metadata or {}
            )

            success = self.sink.emit(event)
            return event.event_id if success else None

        except Exception as e:
            logger.error(f"Failed to capture interaction: {str(e)}")
            return None

class AnalyticsEngine:
    
    @staticmethod
    def identify_bot_behavior(events: List[InteractionEvent]) -> bool:
        if len(events) < 2:
            return False
        
        
        time_diffs = [
            (events[i].timestamp - events[i-1].timestamp).total_seconds()
            for i in range(1, len(events))
        ]
        avg_latency = sum(time_diffs) / len(time_diffs)
        return avg_latency < 0.1  

def bootstrap_tracking_system():
    
    
    stream_sink = KinesisEventSink(stream_name="UserInteractionStream")
    session_mgr = SessionContext()
    tracker = InteractionTracker(sink=stream_sink, session_manager=session_mgr)

    
    test_user = "amzn_user_88291"
    browser_ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"

    
    tracker.capture(
        user_id=test_user,
        event_type="PAGE_VIEW",
        page_url="https://www.amazon.com/dp/B08L5M6S52",
        user_agent=browser_ua
    )

    
    tracker.capture(
        user_id=test_user,
        event_type="UI_INTERACTION",
        page_url="https://www.amazon.com/dp/B08L5M6S52",
        user_agent=browser_ua,
        metadata={
            "element_id": "passkey-promo-banner",
            "action": "click",
            "component": "device-auth-module"
        }
    )

    
    tracker.capture(
        user_id=test_user,
        event_type="ACCOUNT_LINK_INITIATED",
        page_url="https://www.amazon.com/ap/signin",
        user_agent=browser_ua,
        metadata={
            "provider": "ExternalPartner",
            "auth_method": "OIDC"
        }
    )

if __name__ == "__main__":
    bootstrap_tracking_system()