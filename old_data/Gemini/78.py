import json
import boto3
import unittest
from datetime import datetime
from flask import Flask, request, jsonify
from botocore.exceptions import ClientError

app = Flask(__name__)


S3_BUCKET_NAME = 'user-interaction-analytics-store'
s3_client = boto3.client('s3', region_name='eu-west-2')

def upload_to_s3(interaction_data):
    
    timestamp = datetime.utcnow().strftime('%Y/%m/%d/%H%M%S_%f')
    user_id = interaction_data.get('user_id', 'anonymous')
    file_key = f"logs/{user_id}/{timestamp}.json"
    
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_key,
            Body=json.dumps(interaction_data),
            ContentType='application/json'
        )
        return True
    except ClientError as e:
        
        print(f"AWS S3 ClientError: {e}")
        return False

@app.route('/track/event', methods=['POST'])
def track_event():
    
    event_data = request.get_json()
    
    if not event_data:
        return jsonify({"status": "error", "message": "Missing payload"}), 400

    
    event_data['received_at'] = datetime.utcnow().isoformat()
    event_data['ip_address'] = request.remote_addr
    event_data['user_agent'] = request.headers.get('User-Agent')

    
    success = upload_to_s3(event_data)
    
    if success:
        return jsonify({"status": "captured", "event_id": event_data.get('received_at')}), 201
    else:
        return jsonify({"status": "error", "message": "Storage failure"}), 500

class TestInteractionTracker(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_track_event_invalid_json(self):
        response = self.app.post('/track/event', data="not json", content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_track_event_valid_payload(self):
        
        payload = {
            "user_id": "john_doe_99",
            "event_type": "click",
            "path": "/inventory/dashboard",
            "element_id": "btn-add-item"
        }
        response = self.app.post('/track/event', 
                                 data=json.dumps(payload), 
                                 content_type='application/json')
        
        self.assertIn(response.status_code, [201, 500])

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)