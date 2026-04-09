import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import unittest
from fastapi.testclient import TestClient

app = FastAPI(title="UserInteractionTracker")

class InteractionEvent(BaseModel):
    user_id: str = Field(..., example="user_12345")
    event_type: str = Field(..., example="click")
    page_url: str = Field(..., example="https://example.com/pricing")
    element_id: Optional[str] = None
    metadata: Dict[str, Any] = {}

class InteractionRepository:
    
    def __init__(self):
        self._events: List[Dict[str, Any]] = []

    def save_event(self, event: InteractionEvent) -> str:
        event_data = event.dict()
        event_data["id"] = str(uuid.uuid4())
        event_data["timestamp"] = datetime.utcnow().isoformat()
        self._events.append(event_data)
        return event_data["id"]

    def get_all_events(self) -> List[Dict[str, Any]]:
        return self._events

repo = InteractionRepository()

@app.post("/api/v1/track", status_code=201)
async def track_interaction(event: InteractionEvent):
    try:
        event_id = repo.save_event(event)
        return {"status": "success", "event_id": event_id}
    except Exception as e:
        
        print(f"Error tracking event: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/v1/events")
async def get_events():
    return repo.get_all_events()

class TestInteractionAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
        repo._events = []

    def test_track_event_success(self):
        payload = {
            "user_id": "bristol_grad_2023",
            "event_type": "button_click",
            "page_url": "https://startup-inventory.io/dashboard",
            "metadata": {"button_color": "blue"}
        }
        response = self.client.post("/api/v1/track", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("event_id", response.json())

    def test_get_events_returns_data(self):
        payload = {
            "user_id": "test_user",
            "event_type": "page_view",
            "page_url": "https://example.com"
        }
        self.client.post("/api/v1/track", json=payload)
        response = self.client.get("/api/v1/events")
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["user_id"], "test_user")

    def test_invalid_payload(self):
        
        payload = {"user_id": "test_user"}
        response = self.client.post("/api/v1/track", json=payload)
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    
    
    unittest.main()