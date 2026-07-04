import boto3
from botocore.exceptions import ClientError
import json
import os
import hashlib
import unittest

class Database:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        self.table_name = os.environ.get('TABLE_NAME', 'BicycleShop')

    def create_table(self):
        try:
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'item_id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'item_id',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.wait_until_exists()
            return f"Table {self.table_name} created successfully."
        except ClientError as e:
            return e.response['Error']['Message']

    def add_item(self, item_id, item_name, price):
        item_id_hashed = hashlib.sha256(item_id.encode()).hexdigest()
        table = self.dynamodb.Table(self.table_name)
        try:
            table.put_item(
                Item={
                    'item_id': item_id_hashed,
                    'item_name': item_name,
                    'price': price
                }
            )
            return f"Item {item_name} added successfully."
        except ClientError as e:
            return e.response['Error']['Message']

    def get_item(self, item_id):
        item_id_hashed = hashlib.sha256(item_id.encode()).hexdigest()
        table = self.dynamodb.Table(self.table_name)
        try:
            response = table.get_item(Key={'item_id': item_id_hashed})
            return response.get('Item', None)
        except ClientError as e:
            return e.response['Error']['Message']

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db = Database()
        self.db.create_table()

    def test_add_item(self):
        response = self.db.add_item('1', 'Mountain Bike', 500)
        self.assertIn('added successfully', response)

    def test_get_item(self):
        self.db.add_item('1', 'Mountain Bike', 500)
        item = self.db.get_item('1')
        self.assertIsNotNone(item)
        self.assertEqual(item['item_name'], 'Mountain Bike')

    def tearDown(self):
        self.db.dynamodb.Table(self.db.table_name).delete()
        self.db.dynamodb.Table(self.db.table_name).wait_until_not_exists()

if __name__ == '__main__':
    unittest.main()