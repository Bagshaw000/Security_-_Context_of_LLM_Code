import json
import boto3
import unittest
from datetime import datetime
from flask import Flask, request, jsonify
from unittest.mock import MagicMock, patch


app = Flask(__name__)




dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
table = dynamodb.Table('UserInteractions')

@app.route('/api/v1/track', methods=['POST'])
def track_interaction():
    
    event_data = request.get_json()

    
    if not event_data or 'user_id' not in event_data or 'event_type' not in event_data:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    
    interaction_record = {
        'interaction_id': f"{event_data['user_id']}-{datetime.utcnow().timestamp()}",
        'user_id': event_data['user_id'],
        'event_type': event_data['event_type'],
        'page_url': event_data.get('page_url', 'unknown'),
        'timestamp': datetime.utcnow().isoformat(),
        'browser_info': request.headers.get('User-Agent'),
        'ip_address': request.remote_addr,
        'metadata': event_data.get('metadata', {})
    }

    try:
        
        table.put_item(Item=interaction_record)
        return jsonify({"status": "success", "id": interaction_record['interaction_id']}), 201
    except Exception as e:
        
        return jsonify({"status": "error", "message": str(e)}), 500



class TestInteractionTracker(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('boto3.resource')
    def test_track_interaction_success(self, mock_resource):
        
        mock_table = MagicMock()
        mock_resource.return_value.Table.return_value = mock_table
        
        test_payload = {
            "user_id": "user_12345",
            "event_type": "click_signup",
            "page_url": "/landing-page",
            "metadata": {"element_id": "hero-cta"}
        }
        
        response = self.app.post('/api/v1/track', 
                                 data=json.dumps(test_payload),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'success', response.data)

    def test_track_interaction_invalid_data(self):
        
        invalid_payload = {"user_id": "user_12345"}
        response = self.app.post('/api/v1/track', 
                                 data=json.dumps(invalid_payload),
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInteractionTracker)
    test_result = unittest.TextTestRunner(verbosity=1).run(suite)
    
    if test_result.wasSuccessful():
        print("Unit tests passed. Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("Unit tests failed. Aborting startup.")