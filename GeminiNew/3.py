import os
import uuid
import boto3
import logging
import html
from flask import Flask, request, jsonify, abort
from pydantic import BaseModel, Field, ValidationError, validator
from botocore.exceptions import ClientError
from typing import List, Optional
from unittest import TestCase, main
from unittest.mock import MagicMock, patch




















logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


TABLE_NAME = os.environ.get('DYNAMODB_TABLE', 'TodoItems')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')


dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

class TodoSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = False

    @validator('title', 'description')
    def sanitize_strings(cls, v):
        if v is None:
            return v
        
        return html.escape(v)

class TodoUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None

    @validator('title', 'description')
    def sanitize_strings(cls, v):
        if v is None:
            return v
        return html.escape(v)

def require_auth(f):
    
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning("Unauthorized access attempt detected.")
            return jsonify({"error": "Unauthorized"}), 401
        
        
        request.user_id = "user_123" 
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/todos', methods=['POST'])
@require_auth
def create_todo():
    try:
        data = request.get_json()
        todo_data = TodoSchema(**data)
        
        todo_id = str(uuid.uuid4())
        item = {
            'PK': f"USER
            'SK': f"TODO
            'id': todo_id,
            'user_id': request.user_id,
            'title': todo_data.title,
            'description': todo_data.description,
            'completed': todo_data.completed
        }
        
        table.put_item(Item=item)
        return jsonify(item), 201
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ClientError as e:
        logger.error(f"DynamoDB Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/todos', methods=['GET'])
@require_auth
def get_todos():
    try:
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('PK').eq(f"USER
        )
        return jsonify(response.get('Items', [])), 200
    except ClientError as e:
        logger.error(f"DynamoDB Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/todos/<todo_id>', methods=['PUT'])
@require_auth
def update_todo(todo_id):
    try:
        
        uuid.UUID(todo_id)
        
        data = request.get_json()
        update_data = TodoUpdateSchema(**data)
        update_dict = update_data.dict(exclude_unset=True)
        
        if not update_dict:
            return jsonify({"error": "No update fields provided"}), 400

        expression = "set " + ", ".join(f"
        attr_names = {f"
        attr_values = {f":{k}": v for k, v in update_dict.items()}

        response = table.update_item(
            Key={'PK': f"USER
            UpdateExpression=expression,
            ExpressionAttributeNames=attr_names,
            ExpressionAttributeValues=attr_values,
            ReturnValues="ALL_NEW",
            ConditionExpression="attribute_exists(PK)"
        )
        return jsonify(response.get('Attributes')), 200
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400
    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return jsonify({"error": "Todo not found"}), 404
        logger.error(f"DynamoDB Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/todos/<todo_id>', methods=['DELETE'])
@require_auth
def delete_todo(todo_id):
    try:
        uuid.UUID(todo_id)
        table.delete_item(
            Key={'PK': f"USER
        )
        return '', 204
    except ValueError:
        return jsonify({"error": "Invalid ID format"}), 400
    except ClientError as e:
        logger.error(f"DynamoDB Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500



class TodoAppTests(TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.headers = {'Authorization': 'Bearer mock-token'}

    @patch('__main__.table')
    def test_create_todo_success(self, mock_table):
        payload = {"title": "Buy Milk", "description": "Organic preferred"}
        response = self.client.post('/todos', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())
        mock_table.put_item.assert_called_once()

    def test_create_todo_validation_failure(self):
        
        payload = {"title": "a" * 101}
        response = self.client.post('/todos', json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_xss_sanitization(self):
        payload = {"title": "<script>alert('xss')</script>", "description": "<b>Bold</b>"}
        response = self.client.post('/todos', json=payload, headers=self.headers)
        data = response.get_json()
        self.assertNotIn("<script>", data['title'])
        self.assertIn("&lt;script&gt;", data['title'])

    def test_unauthorized_access(self):
        response = self.client.get('/todos')
        self.assertEqual(response.status_code, 401)

    @patch('__main__.table')
    def test_get_todos(self, mock_table):
        mock_table.query.return_value = {'Items': [{'id': '1', 'title': 'Test'}]}
        response = self.client.get('/todos', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    @patch('__main__.table')
    def test_update_todo_not_found(self, mock_table):
        mock_table.update_item.side_effect = ClientError(
            {"Error": {"Code": "ConditionalCheckFailedException"}}, "UpdateItem"
        )
        valid_uuid = str(uuid.uuid4())
        response = self.client.put(f'/todos/{valid_uuid}', json={"completed": True}, headers=self.headers)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    
    
    main()