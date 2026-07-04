import json
import time
import uuid
import logging
import unittest
from datetime import datetime
from flask import Flask, request, jsonify


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("UserInteractionTracker")

class InteractionStore:
    
    def __init__(self):
        self.db = []

    def save_event(self, event_data):
        event_data['event_id'] = str(uuid.uuid4())
        event_data['received_at'] = datetime.utcnow().isoformat()
        self.db.append(event_data)
        logger.info(f"Stored event: {event_data['event_id']} for user: {event_data.get('user_id')}")
        return event_data['event_id']

    def get_all_events(self):
        return self.db

app = Flask(__name__)
store = InteractionStore()

@app.route('/api/v1/track', methods=['POST'])
def track_interaction():
    
    data = request.get_json()

    if not data or 'user_id' not in data or 'event_type' not in data:
        return jsonify({"error": "Invalid payload. user_id and event_type are required."}), 400

    try:
        event_id = store.save_event(data)
        return jsonify({"status": "success", "event_id": event_id}), 201
    except Exception as e:
        logger.error(f"Failed to track interaction: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()}), 200

class TestTrackingSystem(unittest.TestCase):
    
    def setUp(self):
        self.store = InteractionStore()
        self.sample_event = {
            "user_id": "test_user_789",
            "event_type": "page_view",
            "url": "/home",
            "metadata": {"browser": "Chrome"}
        }

    def test_event_storage(self):
        event_id = self.store.save_event(self.sample_event)
        self.assertIsInstance(event_id, str)
        self.assertEqual(len(self.store.get_all_events()), 1)

    def test_event_data_integrity(self):
        self.store.save_event(self.sample_event)
        retrieved = self.store.get_all_events()[0]
        self.assertEqual(retrieved['user_id'], "test_user_789")
        self.assertIn('received_at', retrieved)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTrackingSystem)
    unittest.TextTestRunner(verbosity=1).run(suite)

if __name__ == '__main__':
    
    print("Running unit tests...")
    run_tests()
    
    
    print("Starting interaction tracking service...")
    
    app.run(host='0.0.0.0', port=5000)