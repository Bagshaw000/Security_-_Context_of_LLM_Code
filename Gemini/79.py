import json
import uuid
import boto3
import unittest
from datetime import datetime
from flask import Flask, request, jsonify
from unittest.mock import MagicMock


class InteractionService:
    def __init__(self, table_name='WebsiteInteractions'):
        self.dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
        self.table = self.dynamodb.Table(table_name)

    def record_interaction(self, user_id, event_type, element_id, page_url, session_id, metadata=None):
        
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        item = {
            'event_id': event_id,
            'user_id': user_id,
            'session_id': session_id,
            'event_type': event_type,  
            'element_id': element_id,
            'page_url': page_url,
            'timestamp': timestamp,
            'metadata': metadata or {}
        }

        try:
            self.table.put_item(Item=item)
            return event_id
        except Exception as e:
            
            print(f"Failed to log interaction to DynamoDB: {e}")
            return None


app = Flask(__name__)
tracker_service = InteractionService()

@app.route('/api/v1/collect', methods=['POST'])
def collect_interaction():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided"}), 400

    
    required_fields = ['user_id', 'event_type', 'page_url', 'session_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required tracking fields"}), 400

    event_id = tracker_service.record_interaction(
        user_id=data['user_id'],
        event_type=data['event_type'],
        element_id=data.get('element_id'),
        page_url=data['page_url'],
        session_id=data['session_id'],
        metadata=data.get('metadata')
    )

    if event_id:
        return jsonify({"status": "success", "event_id": event_id}), 201
    else:
        return jsonify({"status": "error", "message": "Internal storage failure"}), 500


class TestInteractionTracking(unittest.TestCase):
    def setUp(self):
        self.service = InteractionService(table_name='TestTable')
        
        self.service.table = MagicMock()

    def test_record_interaction_success(self):
        self.service.table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        
        event_id = self.service.record_interaction(
            user_id='john_doe_bristol',
            event_type='click',
            element_id='signup-btn',
            page_url='https://example.com/home',
            session_id='sess-999'
        )
        
        self.assertIsNotNone(event_id)
        self.assertTrue(self.service.table.put_item.called)

    def test_record_interaction_failure(self):
        
        self.service.table.put_item.side_effect = Exception("DynamoDB Down")
        
        event_id = self.service.record_interaction(
            user_id='test_user',
            event_type='view',
            element_id=None,
            page_url='/shop',
            session_id='abc-123'
        )
        
        self.assertIsNone(event_id)

if __name__ == '__main__':
    
    
    
    
    unittest.main(exit=False)