import boto3
import logging
import uuid
import re
from datetime import datetime
from botocore.exceptions import ClientError
from typing import List, Dict, Optional
import unittest
from unittest.mock import MagicMock


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecureTodoApp:
    

    def __init__(self, region_name: str, user_pool_id: str, client_id: str, table_name: str):
        self.region_name = region_name
        self.user_pool_id = user_pool_id
        self.client_id = client_id
        self.table_name = table_name
        
        
        
        self.cognito = boto3.client('cognito-idp', region_name=self.region_name)
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region_name)
        self.table = self.dynamodb.Table(self.table_name)

    def validate_input(self, text: str, max_length: int = 500) -> bool:
        
        if not text or not isinstance(text, str):
            return False
        if len(text.strip()) == 0 or len(text) > max_length:
            return False
        
        return bool(re.match(r"^[a-zA-Z0-9\s.,!?-]+$", text))

    def register_user(self, username: str, password: str, email: str) -> bool:
        
        try:
            self.cognito.sign_up(
                ClientId=self.client_id,
                Username=username,
                Password=password,
                UserAttributes=[{'Name': 'email', 'Value': email}]
            )
            logger.info(f"User {username} registered successfully.")
            return True
        except ClientError as e:
            logger.error(f"Registration error: {e.response['Error']['Message']}")
            return False

    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        
        try:
            response = self.cognito.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                },
                ClientId=self.client_id
            )
            return response['AuthenticationResult']['AccessToken']
        except ClientError as e:
            logger.error(f"Authentication failed for {username}: {e.response['Error']['Message']}")
            return None

    def create_todo(self, user_id: str, task_content: str) -> bool:
        
        if not self.validate_input(task_content):
            logger.warning(f"Invalid input detected for user {user_id}")
            return False

        todo_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        try:
            self.table.put_item(
                Item={
                    'user_id': user_id,  
                    'todo_id': todo_id,  
                    'content': task_content,
                    'created_at': timestamp,
                    'status': 'pending'
                },
                
                ConditionExpression="attribute_not_exists(todo_id)"
            )
            return True
        except ClientError as e:
            logger.error(f"Data storage error: {e.response['Error']['Message']}")
            return False

    def get_user_todos(self, user_id: str) -> List[Dict]:
        
        try:
            response = self.table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
            )
            return response.get('Items', [])
        except ClientError as e:
            logger.error(f"Retrieval error: {e.response['Error']['Message']}")
            return []

    def delete_todo(self, user_id: str, todo_id: str) -> bool:
        
        try:
            self.table.delete_item(
                Key={'user_id': user_id, 'todo_id': todo_id},
                
                ConditionExpression="attribute_exists(user_id) AND user_id = :u",
                ExpressionAttributeValues={":u": user_id}
            )
            return True
        except ClientError as e:
            logger.error(f"Deletion error: {e.response['Error']['Message']}")
            return False

class TestSecureTodoApp(unittest.TestCase):
    

    def setUp(self):
        
        self.app = SecureTodoApp("us-east-1", "mock_pool", "mock_client", "mock_table")
        self.app.table = MagicMock()
        self.app.cognito = MagicMock()

    def test_input_validation_valid(self):
        self.assertTrue(self.app.validate_input("Buy groceries."))

    def test_input_validation_invalid_script(self):
        self.assertFalse(self.app.validate_input("<script>alert(1)</script>"))

    def test_input_validation_too_long(self):
        self.assertFalse(self.app.validate_input("a" * 501))

    def test_create_todo_success(self):
        self.app.table.put_item.return_value = {}
        result = self.app.create_todo("user123", "Finish project report")
        self.assertTrue(result)

    def test_create_todo_failure_invalid_input(self):
        result = self.app.create_todo("user123", "")
        self.assertFalse(result)









if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSecureTodoApp)
    unittest.TextTestRunner(verbosity=2).run(suite)

    
    
    
    
    
    
    