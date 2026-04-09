import uuid
import json
import threading
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

class InteractionEvent:
    
    __slots__ = ['event_id', 'user_id', 'session_id', 'event_type', 'schema_version', 'timestamp', 'metadata']
    
    def __init__(self, user_id: str, session_id: str, event_type: str, metadata: Dict[str, Any]):
        self.event_id = str(uuid.uuid4())
        self.user_id = user_id
        self.session_id = session_id
        self.event_type = event_type
        self.schema_version = "1.0.2"
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.metadata = metadata

    def to_json(self) -> str:
        return json.dumps({
            "header": {
                "event_id": self.event_id,
                "schema_version": self.schema_version,
                "timestamp": self.timestamp
            },
            "identity": {
                "user_id": self.user_id,
                "session_id": self.session_id
            },
            "payload": {
                "action": self.event_type,
                "data": self.metadata
            }
        })

class EventIngestor(ABC):
    
    @abstractmethod
    def emit(self, event: InteractionEvent) -> None:
        pass

    @abstractmethod
    def shutdown(self) -> None:
        pass

class KinesisBufferedIngestor(EventIngestor):
    
    def __init__(self, stream_name: str, batch_size: int = 10, flush_interval_sec: int = 5):
        self.stream_name = stream_name
        self.batch_size = batch_size
        self.flush_interval_sec = flush_interval_sec
        self._buffer: List[InteractionEvent] = []
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._flush_thread = threading.Thread(target=self._periodic_flush, daemon=True)
        self._flush_thread.start()

    def emit(self, event: InteractionEvent) -> None:
        with self._lock:
            self._buffer.append(event)
            if len(self._buffer) >= self.batch_size:
                self._flush_internal()

    def _periodic_flush(self) -> None:
        while not self._stop_event.is_set():
            time.sleep(self.flush_interval_sec)
            with self._lock:
                if self._buffer:
                    self._flush_internal()

    def _flush_internal(self) -> None:
        if not self._buffer:
            return
        
        
        records_to_send = [e.to_json() for e in self._buffer]
        print(f"[INGESTOR] flushing {len(records_to_send)} records to {self.stream_name}...")
        
        
        self._buffer.clear()

    def shutdown(self) -> None:
        self._stop_event.set()
        with self._lock:
            self._flush_internal()
        self._flush_thread.join(timeout=2.0)

class InteractionTracker:
    
    _instance: Optional['InteractionTracker'] = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(InteractionTracker, cls).__new__(cls)
            return cls._instance

    def __init__(self, ingestor: Optional[EventIngestor] = None):
        if not hasattr(self, 'initialized'):
            self.ingestor = ingestor or KinesisBufferedIngestor("web-interactions-stream")
            self.initialized = True

    def track(self, user_id: str, session_id: str, action: str, **context: Any) -> None:
        event = InteractionEvent(
            user_id=user_id,
            session_id=session_id,
            event_type=action,
            metadata=context
        )
        self.ingestor.emit(event)

    def track_page_view(self, user_id: str, session_id: str, url: str, referrer: str = "") -> None:
        self.track(user_id, session_id, "PAGE_VIEW", url=url, referrer=referrer)

    def track_click(self, user_id: str, session_id: str, element_id: str, url: str) -> None:
        self.track(user_id, session_id, "CLICK", element_id=element_id, url=url)


if __name__ == "__main__":
    
    tracker = InteractionTracker()

    
    def simulate_user_session(uid: str):
        sid = f"sess_{uuid.uuid4().hex[:12]}"
        tracker.track_page_view(uid, sid, "https://amazon.com/dp/B08N5WRWJ6")
        time.sleep(0.1)
        tracker.track_click(uid, sid, "add-to-cart-button", "https://amazon.com/dp/B08N5WRWJ6")
        tracker.track(uid, sid, "AUTH_CHALLENGE_INITIATED", method="passkey")

    threads = []
    for i in range(5):
        t = threading.Thread(target=simulate_user_session, args=(f"user_{i}",))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    
    if isinstance(tracker.ingestor, KinesisBufferedIngestor):
        tracker.ingestor.shutdown()