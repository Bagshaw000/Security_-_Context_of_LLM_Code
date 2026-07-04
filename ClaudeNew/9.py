import os
import json
import logging
from functools import wraps
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable
import hashlib
import secrets
from enum import Enum

import jwt
from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest
import boto3
from botocore.exceptions import ClientError
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import text
import unittest
from unittest.mock import patch, MagicMock
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.getenv('ALLOWED_ORIGINS', 'https://localhost:3000').split(',')}})

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

Base = declarative_base()

class UserRole(Enum):
    ADMIN = "admin"
    CONTENT_CREATOR = "content_creator"
    VIEWER = "viewer"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default=UserRole.VIEWER.value)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class Video(Base):
    __tablename__ = 'videos'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    uploader_id = Column(Integer, nullable=False)
    s3_key = Column(String(500), unique=True, nullable=False)
    duration = Column(Integer, nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String(255), nullable=False)
    resource = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45), nullable=False)
    details = Column(Text, nullable=True)

class SecurityConfig:
    def __init__(self):
        self.jwt_secret = os.getenv('JWT_SECRET')
        if not self.jwt_secret:
            raise ValueError("JWT_SECRET must be set in environment variables")
        
        self.jwt_algorithm = "HS256"
        self.token_expiration_hours = int(os.getenv('TOKEN_EXPIRATION_HOURS', 24))
        self.database_url = os.getenv('DATABASE_URL')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.s3_bucket = os.getenv('S3_BUCKET')
        self.cloudfront_domain = os.getenv('CLOUDFRONT_DOMAIN')
        self.max_video_size_mb = int(os.getenv('MAX_VIDEO_SIZE_MB', 5000))
        self.allowed_video_extensions = {'mp4', 'webm', 'mov', 'avi'}
        
        if not all([self.database_url, self.s3_bucket, self.cloudfront_domain]):
            raise ValueError("Required environment variables not set")

app.config['SECURITY_CONFIG'] = SecurityConfig()

engine = create_engine(
    app.config['SECURITY_CONFIG'].database_url,
    pool_pre_ping=True,
    pool_recycle=3600
)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def sanitize_input(user_input: str, max_length: int = 1000) -> str:
    if not isinstance(user_input, str):
        raise ValueError("Input must be a string")
    
    if len(user_input) > max_length:
        raise ValueError(f"Input exceeds maximum length of {max_length}")
    
    user_input = user_input.strip()
    
    dangerous_patterns = ['<script', 'onclick=', 'onerror=', 'javascript:', 'union select', 'drop table']
    lower_input = user_input.lower()
    for pattern in dangerous_patterns:
        if pattern in lower_input:
            raise ValueError(f"Input contains potentially dangerous content: {pattern}")
    
    return user_input

def encode_jwt_token(user_id: int, role: str) -> str:
    payload = {
        'user_id': user_id,
        'role': role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(hours=app.config['SECURITY_CONFIG'].token_expiration_hours),
        'jti': secrets.token_hex(16)
    }
    
    token = jwt.encode(
        payload,
        app.config['SECURITY_CONFIG'].jwt_secret,
        algorithm=app.config['SECURITY_CONFIG'].jwt_algorithm
    )
    return token

def decode_jwt_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            app.config['SECURITY_CONFIG'].jwt_secret,
            algorithms=[app.config['SECURITY_CONFIG'].jwt_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {str(e)}")

def require_auth(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'Missing authorization token'}), 401
        
        try:
            payload = decode_jwt_token(token)
            request.user_id = payload['user_id']
            request.user_role = payload['role']
        except ValueError as e:
            logger.warning(f"Authentication failed: {str(e)}")
            return jsonify({'error': 'Unauthorized'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_role(*allowed_roles: str) -> Callable:
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(request, 'user_role') or request.user_role not in allowed_roles:
                logger.warning(f"Authorization failed for role: {getattr(request, 'user_role', 'unknown')}")
                return jsonify({'error': 'Insufficient permissions'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def log_audit_event(user_id: Optional[int], action: str, resource: str, details: Optional[str] = None):
    db = SessionLocal()
    try:
        ip_address = request.remote_addr or 'unknown'
        
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            details=details
        )
        db.add(audit_log)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log audit event: {str(e)}")
        db.rollback()
    finally:
        db.close()

def get_s3_client():
    return boto3.client(
        's3',
        region_name=app.config['SECURITY_CONFIG'].aws_region,
        config=boto3.session.Config(
            signature_version='s3v4',
            retries={'max_attempts': 3, 'mode': 'standard'}
        )
    )

def get_secrets_manager_client():
    return boto3.client(
        'secretsmanager',
        region_name=app.config['SECURITY_CONFIG'].aws_region
    )

def get_secret(secret_name: str) -> Dict[str, Any]:
    client = get_secrets_manager_client()
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            return json.loads(response['SecretString'])
        return json.loads(response['SecretBinary'])
    except ClientError as e:
        logger.error(f"Failed to retrieve secret: {str(e)}")
        raise

@app.route('/api/health', methods=['GET'])
@limiter.limit("10 per minute")
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}), 200

@app.route('/api/auth/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        username = sanitize_input(data['username'], 255)
        email = sanitize_input(data['email'], 255)
        password = data['password']
        
        if len(password) < 12:
            return jsonify({'error': 'Password must be at least 12 characters long'}), 400
        
        if not all(c.isupper() or c.islower() or c.isdigit() or c in '!@
            return jsonify({'error': 'Password must contain uppercase, lowercase, digits, and special characters'}), 400
        
        db = SessionLocal()
        try:
            existing_user = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                log_audit_event(None, 'REGISTER_FAILED', 'users', f'Duplicate username or email: {username}')
                return jsonify({'error': 'Username or email already exists'}), 409
            
            password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=32)
            
            new_user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=UserRole.VIEWER.value,
                is_active=True
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            log_audit_event(new_user.id, 'REGISTER', 'users', f'User registered: {username}')
            
            return jsonify({
                'message': 'Registration successful',
                'user_id': new_user.id
            }), 201
        
        except Exception as e:
            db.rollback()
            logger.error(f"Registration error: {str(e)}")
            return jsonify({'error': 'Registration failed'}), 500
        finally:
            db.close()
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per hour")
def login():
    try:
        data = request.get_json()
        
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        username = sanitize_input(data['username'], 255)
        password = data['password']
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            
            if not user or not user.is_active:
                log_audit_event(None, 'LOGIN_FAILED', 'users', f'Invalid credentials for username: {username}')
                return jsonify({'error': 'Invalid credentials'}), 401
            
            if not check_password_hash(user.password_hash, password):
                log_audit_event(user.id, 'LOGIN_FAILED', 'users', 'Invalid password')
                return jsonify({'error': 'Invalid credentials'}), 401
            
            user.last_login = datetime.utcnow()
            db.commit()
            
            token = encode_jwt_token(user.id, user.role)
            
            log_audit_event(user.id, 'LOGIN_SUCCESS', 'users', f'User logged in')
            
            return jsonify({
                'token': token,
                'user_id': user.id,
                'role': user.role,
                'expires_in': app.config['SECURITY_CONFIG'].token_expiration_hours * 3600
            }), 200
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return jsonify({'error': 'Login failed'}), 500
        finally:
            db.close()
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/videos/upload', methods=['POST'])
@limiter.limit("5 per hour")
@require_auth
@require_role(UserRole.CONTENT_CREATOR.value, UserRole.ADMIN.value)
def upload_video():
    try:
        if 'file' not in request.files or 'title' not in request.form:
            return jsonify({'error': 'Missing file or title'}), 400
        
        file = request.files['file']
        title = sanitize_input(request.form['title'], 500)
        description = sanitize_input(request.form.get('description', ''), 2000)
        is_public = request.form.get('is_public', 'false').lower() == 'true'
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_extension not in app.config['SECURITY_CONFIG'].allowed_video_extensions:
            return jsonify({'error': f'Invalid file type. Allowed: {app.config["SECURITY_CONFIG"].allowed_video_extensions}'}), 400
        
        file_size_mb = len(file.read()) / (1024 * 1024)
        file.seek(0)
        
        if file_size_mb > app.config['SECURITY_CONFIG'].max_video_size_mb:
            return jsonify({'error': f