import boto3
import json
import os
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from botocore.exceptions import ClientError
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserInteractions')

logging.basicConfig(level=logging.INFO)

def log_interaction(user_id, interaction_data):
    try:
        response = table.put_item(
            Item={
                'UserId': user_id,
                'InteractionData': json.dumps(interaction_data)
            }
        )
        logging.info(f"Logged interaction for user {user_id}: {interaction_data}")
        return response
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
        return None

@app.route('/track', methods=['POST'])
def track_interaction():
    data = request.get_json()
    user_id = data.get('user_id')
    interaction_data = data.get('interaction_data')

    if not user_id or not interaction_data:
        return jsonify({'error': 'Invalid input'}), 400

    log_interaction(user_id, interaction_data)
    return jsonify({'message': 'Interaction logged successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)


import unittest
from unittest.mock import patch

class TestUserInteractionTracking(unittest.TestCase):

    @patch('boto3.resource')
    def test_log_interaction_success(self, mock_boto):
        mock_table = mock_boto.return_value.Table.return_value
        mock_table.put_item.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}

        response = log_interaction('test_user', {'action': 'click', 'element': 'button'})
        self.assertIsNotNone(response)
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

    @patch('boto3.resource')
    def test_log_interaction_failure(self, mock_boto):
        mock_table = mock_boto.return_value.Table.return_value
        mock_table.put_item.side_effect = ClientError(
            {"Error": {"Code": "InternalError", "Message": "Internal error"}}, "PutItem"
        )

        response = log_interaction('test_user', {'action': 'click', 'element': 'button'})
        self.assertIsNone(response)

if __name__ == '__main__':
    unittest.main()