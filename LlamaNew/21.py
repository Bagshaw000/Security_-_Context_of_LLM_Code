import os
import json
import boto3
import unittest
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
from cryptography.fernet import Fernet
from botocore.exceptions import ClientError





ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

def encrypt_token(token: str) -> str:
    return cipher_suite.encrypt(token.encode()).decode()

def decrypt_token(encrypted_token: str) -> str:
    return cipher_suite.decrypt(encrypted_token.encode()).decode()



class WorkoutSet(BaseModel):
    exercise_name: str = Field(..., min_length=1, max_length=100)
    reps: int = Field(..., gt=0, lt=1000)
    weight: float = Field(..., ge=0)

class WorkoutSession(BaseModel):
    user_id: str
    timestamp: datetime
    source_app: str
    exercises: List[WorkoutSet]

    @validator('source_app')
    def validate_source(cls, v):
        allowed_sources = ['Strava', 'AppleHealth', 'MyFitnessPal', 'Manual']
        if v not in allowed_sources:
            raise ValueError('Invalid source application')
        return v



class WorkoutRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.table = self.dynamodb.Table('WorkoutLogs')

    def save_workout(self, workout: WorkoutSession):
        try:
            self.table.put_item(Item=workout.dict())
        except ClientError as e:
            raise HTTPException(status_code=500, detail="Database write error")

class ExternalAppIntegrator:
    
    def __init__(self, api_key_encrypted: str):
        self.api_key = decrypt_token(api_key_encrypted)

    def fetch_external_data(self, external_user_id: str):
        
        
        mock_response = {
            "user_id": "user123",
            "timestamp": datetime.utcnow().isoformat(),
            "source_app": "Strava",
            "exercises": [{"exercise_name": "Deadlift", "reps": 5, "weight": 100.0}]
        }
        return mock_response



app = FastAPI()
auth_scheme = HTTPBearer()
repo = WorkoutRepository()

@app.post("/import/{provider}")
async def import_workout(provider: str, token: HTTPAuthorizationCredentials = Security(auth_scheme)):
    
    if provider not in ['strava', 'apple']:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    
    
    encrypted_token = encrypt_token(token.credentials)
    integrator = ExternalAppIntegrator(encrypted_token)
    
    
    raw_data = integrator.fetch_external_data("ext_999")
    try:
        workout = WorkoutSession(**raw_data)
        repo.save_workout(workout)
        return {"status": "success", "data_imported": workout.timestamp}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))



class TestWorkoutApp(unittest.TestCase):
    def setUp(self):
        self.valid_payload = {
            "user_id": "test_user",
            "timestamp": datetime.utcnow(),
            "source_app": "Strava",
            "exercises": [{"exercise_name": "Squat", "reps": 10, "weight": 60.5}]
        }

    def test_validation_success(self):
        session = WorkoutSession(**self.valid_payload)
        self.assertEqual(session.source_app, "Strava")

    def test_validation_failure_invalid_source(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload["source_app"] = "UnknownApp"
        with self.assertRaises(ValueError):
            WorkoutSession(**invalid_payload)

    def test_encryption_roundtrip(self):
        original = "secret_api_token_123"
        encrypted = encrypt_token(original)
        decrypted = decrypt_token(encrypted)
        self.assertEqual(original, decrypted)
        self.assertNotEqual(original, encrypted)




if __name__ == "__main__":
    
    unittest.main()