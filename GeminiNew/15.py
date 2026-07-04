import json
import boto3
import hashlib
import re
import os
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch


STREAM_NAME = os.environ.get('KINESIS_STREAM_NAME', 'user-interactions-stream')

kinesis_client = boto3.client('kinesis', region_name='eu-west-2')

def sanitize_input(text):
    
    if not isinstance(text, str):
        return str(text)
    
    return re.sub(r'[<>&"\']', '', text).strip()

def anonymize_pii(value, salt="bristol_cs_security_salt_2023"):
    
    if not value:
        return "anonymous"
    
    hash_obj = hashlib.sha256((value + salt).encode('utf-8'))
    return hash_obj.hexdigest()

def validate_interaction_type(interaction_type):
    
    allowed_types = {'page_view', 'click', 'session_duration'}
    sanitized = sanitize_input(interaction_type)
    return sanitized if sanitized in allowed_types else 'unknown_interaction'

def process_telemetry(raw_body, client_ip):
    
    
    user_id = raw_body.get('user_id', 'anonymous_user')
    interaction_type = raw_body.get('interaction_type', 'unknown')
    element_id = raw_body.get('element_id', 'none')
    duration = raw_body.get('duration', 0)

    
    processed_data = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id_hash': anonymize_pii(user_id),
        'ip_hash': anonymize_pii(client_ip),
        'interaction_type': validate_interaction_type(interaction_type),
        'element_id': sanitize_input(element_id),
        'duration_seconds': float(duration) if str(duration).replace('.','',1).isdigit() else 0.0
    }
    return processed_data

def lambda_handler(event, context):
    
    try:
        
        body_str = event.get('body', '{}')
        body = json.loads(body_str)
        
        
        request_context = event.get('requestContext', {})
        identity = request_context.get('identity', {})
        client_ip = identity.get('sourceIp', '0.0.0.0')

        
        telemetry_record = process_telemetry(body, client_ip)

        
        kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(telemetry_record),
            PartitionKey=telemetry_record['user_id_hash'] 
        )

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'status': 'success', 'tracking_id': telemetry_record['user_id_hash'][:8]})
        }

    except json.JSONDecodeError:
        return {'statusCode': 400, 'body': json.dumps({'error': 'Invalid JSON format'})}
    except Exception as e:
        
        print(f"Internal Error: {str(e)}")
        return {'statusCode': 500, 'body': json.dumps({'error': 'Internal Server Error'})}



class TestUserTrackingModule(unittest.TestCase):
    
    def test_sanitization_logic(self):
        malicious_input = "<script>alert('xss')</script>"
        clean_output = sanitize_input(malicious_input)
        self.assertNotIn("<script>", clean_output)
        self.assertNotIn("'", clean_output)
        self.assertEqual(clean_output, "scriptalert(xss)/script")

    def test_pii_anonymization(self):
        ip = "192.168.1.50"
        hashed_ip = anonymize_pii(ip)
        self.assertNotEqual(ip, hashed_ip)
        self.assertEqual(len(hashed_ip), 64) 
        
        self.assertEqual(hashed_ip, anonymize_pii(ip))

    def test_interaction_validation(self):
        self.assertEqual(validate_interaction_type('click'), 'click')
        self.assertEqual(validate_interaction_type('drop_database'), 'unknown_interaction')

    def test_telemetry_processing_structure(self):
        raw = {'user_id': 'john123', 'interaction_type': 'page_view', 'duration': '45.5'}
        processed = process_telemetry(raw, "127.0.0.1")
        self.assertIn('timestamp', processed)
        self.assertIsInstance(processed['duration_seconds'], float)
        self.assertEqual(processed['duration_seconds'], 45.5)

    @patch('boto3.client')
    def test_lambda_handler_integration(self, mock_boto):
        
        mock_kinesis = MagicMock()
        mock_boto.return_value = mock_kinesis
        
        test_event = {
            'body': json.dumps({
                'user_id': 'test_user',
                'interaction_type': 'click',
                'element_id': 'nav_home'
            }),
            'requestContext': {'identity': {'sourceIp': '1.1.1.1'}}
        }
        
        response = lambda_handler(test_event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertTrue(mock_kinesis.put_record.called)

if __name__ == "__main__":
    
    unittest.main()
