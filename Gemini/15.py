import json
import time
import uuid
from datetime import datetime
import boto3
from botocore.exceptions import ClientError
import unittest

class InteractionTracker:
    
    def __init__(self, table_name='UserEvents', region_name='eu-west-2'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table_name = table_name
        self.table = self.dynamodb.Table(table_name)

    def track_event(self, user_id, session_id, url, event_type, element_id=None, metadata=None):
        
        timestamp = datetime.utcnow().isoformat()
        event_id = str(uuid.uuid4())
        
        item = {
            'event_id': event_id,
            'user_id': user_id,
            'session_id': session_id,
            'url': url,
            'event_type': event_type,
            'element_id': element_id,
            'timestamp': timestamp,
            'metadata': metadata or {}
        }
        
        try:
            self.table.put_item(Item=item)
            return {'status': 'success', 'event_id': event_id}
        except ClientError as e:
            return {'status': 'error', 'message': e.response['Error']['Message']}

class TestInteractionTracker(unittest.TestCase):
    
    def test_event_payload_structure(self):
        
        user_id = "bristol_grad_2023"
        session_id = "sess_98765"
        url = "/inventory/manage"
        event_type = "click"
        
        
        self.assertIsNotNone(user_id)
        self.assertTrue(url.startswith('/'))

    def test_timestamp_format(self):
        now = datetime.utcnow().isoformat()
        self.assertIsInstance(now, str)
        self.assertIn('T', now)

def lambda_handler(event, context):
    
    tracker = InteractionTracker()
    
    try:
        body = json.loads(event.get('body', '{}'))
        
        result = tracker.track_event(
            user_id=body.get('user_id'),
            session_id=body.get('session_id'),
            url=body.get('url'),
            event_type=body.get('event_type'),
            element_id=body.get('element_id'),
            metadata=body.get('metadata')
        )
        
        return {
            'statusCode': 200 if result['status'] == 'success' else 500,
            'body': json.dumps(result)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': str(e)})
        }

if __name__ == "__main__":
    
    print("Initializing Tracker...")
    
    example_tracker = InteractionTracker(table_name='DevelopmentEvents')
    
    sample_log = example_tracker.track_event(
        user_id="john_doe_123",
        session_id="abc-123-xyz",
        url="https://startup-inventory-tool.io/dashboard",
        event_type="view_report",
        element_id="btn_generate_pdf",
        metadata={"browser": "Chrome", "resolution": "1920x1080"}
    )
    print(f"Tracking Result: {sample_log}")
    
    
    unittest.main(exit=False)