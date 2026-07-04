import os
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json
import hmac

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from fastapi.responses import JSONResponse
import sqlalchemy
from sqlalchemy import create_engine, Column, String, DateTime, LargeBinary, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import boto3
import httpx
from pydantic import BaseModel, validator, EmailStr
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/workout_db")
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,
    pool_recycle=3600
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Secure Workout Tracker")
app.state.limiter = limiter

secrets_client = boto3.client('secretsmanager', region_name=os.getenv('AWS_REGION', 'us-east-1'))

class EncryptionService:
    def __init__(self):
        self.cipher_suite = self._get_or_create_cipher()
    
    def _get_or_create_cipher(self) -> Fernet:
        try:
            key = secrets_client.get_secret_value(SecretId='workout-app-encryption-key')
            encryption_key = key['SecretString'].encode()
        except Exception as e:
            logger.warning(f"Could not retrieve encryption key from Secrets Manager: {e}")
            encryption_key = os.getenv('ENCRYPTION_KEY', '').encode()
            if not encryption_key or len(encryption_key) < 32:
                raise ValueError("ENCRYPTION_KEY environment variable must be set and valid")
        
        if len(encryption_key) == 32:
            encryption_key = Fernet.generate_key()
        
        return Fernet(encryption_key)
    
    def encrypt(self, plaintext: str) -> str:
        encrypted = self.cipher_suite.encrypt(plaintext.encode())
        return encrypted.decode()
    
    def decrypt(self, ciphertext: str) -> str:
        try:
            decrypted = self.cipher_suite.decrypt(ciphertext.encode())
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise ValueError("Failed to decrypt data")

encryption_service = EncryptionService()

class SecretManager:
    @staticmethod
    def get_secret(secret_name: str) -> str:
        try:
            response = secrets_client.get_secret_value(SecretId=secret_name)
            if 'SecretString' in response:
                return response['SecretString']
            else:
                logger.error(f"Binary secrets not supported: {secret_name}")
                raise ValueError("Unsupported secret format")
        except Exception as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve configuration")
    
    @staticmethod
    def store_secret(secret_name: str, secret_value: str) -> None:
        try:
            secrets_client.create_secret(
                Name=secret_name,
                SecretString=secret_value,
                Tags=[
                    {'Key': 'Application', 'Value': 'WorkoutTracker'},
                    {'Key': 'Environment', 'Value': os.getenv('ENVIRONMENT', 'production')}
                ]
            )
        except secrets_client.exceptions.ResourceExistsException:
            secrets_client.update_secret(
                SecretId=secret_name,
                SecretString=secret_value
            )
        except Exception as e:
            logger.error(f"Failed to store secret {secret_name}: {e}")
            raise HTTPException(status_code=500, detail="Failed to store configuration")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    action = Column(String)
    resource = Column(String)
    status = Column(String)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    details = Column(Text)

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    salt = Column(LargeBinary)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ThirdPartyCredential(Base):
    __tablename__ = "third_party_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    provider = Column(String)
    encrypted_access_token = Column(String)
    encrypted_refresh_token = Column(String)
    token_expiry = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class WorkoutData(Base):
    __tablename__ = "workout_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    provider = Column(String)
    encrypted_metrics = Column(String)
    data_hash = Column(String, unique=True)
    imported_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

class PasswordService:
    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> tuple[str, bytes]:
        if salt is None:
            salt = secrets.token_bytes(32)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000
        )
        key = kdf.derive(password.encode())
        password_hash = key.hex()
        
        return password_hash, salt
    
    @staticmethod
    def verify_password(password: str, stored_hash: str, salt: bytes) -> bool:
        computed_hash, _ = PasswordService.hash_password(password, salt)
        return hmac.compare_digest(computed_hash, stored_hash)

class AuditService:
    @staticmethod
    def log_action(
        db: Session,
        user_id: str,
        action: str,
        resource: str,
        status: str,
        request: Request,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        try:
            client_ip = request.client.host if request.client else "unknown"
            
            audit_entry = AuditLog(
                user_id=user_id,
                action=action,
                resource=resource,
                status=status,
                ip_address=client_ip,
                details=json.dumps(details or {})
            )
            db.add(audit_entry)
            db.commit()
            logger.info(f"Audit log: {action} on {resource} by {user_id} - {status}")
        except Exception as e:
            logger.error(f"Failed to create audit log: {e}")
            db.rollback()

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 12:
            raise ValueError('Password must be at least 12 characters long')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char in '!@
            raise ValueError('Password must contain at least one special character')
        return v

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class WorkoutImportRequest(BaseModel):
    provider: str
    authorization_code: str
    
    @validator('provider')
    def validate_provider(cls, v):
        valid_providers = ['strava', 'myfitnesspal', 'garmin']
        if v.lower() not in valid_providers:
            raise ValueError(f'Provider must be one of {valid_providers}')
        return v.lower()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return {"user_id": user_id, "email": user.email}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(hours=JWT_EXPIRATION_HOURS)
    
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": user_id, "exp": expire}
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

class OAuth2Service:
    OAUTH_CONFIG = {
        'strava': {
            'token_url': 'https://www.strava.com/oauth/token',
            'api_base': 'https://www.strava.com/api/v3',
            'scope': 'read,activity:read_all'
        },
        'myfitnesspal': {
            'token_url': 'https://api.myfitnesspal.com/oauth/token',
            'api_base': 'https://api.myfitnesspal.com/v1',
            'scope': 'fitness_read'
        },
        'garmin': {
            'token_url': 'https://connectapi.garmin.com/oauth-service/oauth/token',
            'api_base': 'https://apis.garmin.com/wellness-api/rest',
            'scope': 'ACTIVITY_READ'
        }
    }
    
    @staticmethod
    def get_oauth_config(provider: str) -> Dict[str, str]:
        provider = provider.lower()
        if provider not in OAuth2Service.OAUTH_CONFIG:
            raise ValueError(f"Unsupported provider: {provider}")
        return OAuth2Service.OAUTH_CONFIG[provider]
    
    @staticmethod
    async def exchange_authorization_code(
        provider: str,
        authorization_code: str
    ) -> Dict[str, Any]:
        provider = provider.lower()
        config = OAuth2Service.get_oauth_config(provider)
        
        try:
            client_id = SecretManager.get_secret(f"{provider}-client-id")
            client_secret = SecretManager.get_secret(f"{provider}-client-secret")
        except Exception as e:
            logger.error(f"Failed to retrieve OAuth credentials for {provider}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve OAuth configuration")
        
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': authorization_code,
            'grant_type': 'authorization_code'
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(config['token_url'], data=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"OAuth token exchange failed for {provider}: {e}")
            raise HTTPException(status_code=401, detail="Failed to authenticate with provider")
    
    @staticmethod
    async def refresh_access_token(
        provider: str,
        refresh_token: str
    ) -> Dict[str, Any]:
        provider = provider.lower()
        config = OAuth2Service.get_oauth_config(provider)
        
        try:
            client_id = SecretManager.get_secret(f"{provider}-client-id")
            client_secret = SecretManager.get_secret(f"{provider}-client-secret")
        except Exception as e:
            logger.error(f"Failed to retrieve OAuth credentials for {provider}: {e}")
            raise HTTPException(status_code=500, detail="Failed to retrieve OAuth configuration")
        
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(config['token_url'], data=payload)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Token refresh failed for {provider}: {e}")
            raise HTTPException(status_code=401, detail="Failed to refresh token")

class DataValidationService:
    VALID_WORKOUT_FIELDS = {
        'duration', 'distance', 'calories', 'heart_rate', 'pace', 
        'activity_type', 'timestamp', 'elevation'
    }
    
    @staticmethod
    def validate_workout_data(data: Dict[str, Any]) -> Dict[str, Any]:
        validated = {}
        
        for key, value in data.items():
            if key not in DataValidationService.VALID_WORKOUT_FIELDS:
                logger.warning(f"Unexpected field in workout data: {key}")
                continue
            
            if key == 'duration':
                if not isinstance(value, (int, float)) or value < 0:
                    