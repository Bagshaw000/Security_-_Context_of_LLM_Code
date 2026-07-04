import os
import sys
import json
import hashlib
import hmac
import logging
import logging.handlers
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple, Union
from enum import Enum
import threading
import time
from functools import wraps
from datetime import datetime, timedelta
import sqlite3
from pathlib import Path
import secrets
import struct

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import numpy as np


class SecurityLevel(Enum):
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    RESTRICTED = 4


class ThreatModel(Enum):
    SINGLE_TENANT = 1
    MULTI_TENANT_ISOLATED = 2
    MULTI_TENANT_SHARED = 3


class AuditEventType(Enum):
    DATA_ACCESS = "DATA_ACCESS"
    MODEL_MODIFICATION = "MODEL_MODIFICATION"
    AUTHENTICATION_SUCCESS = "AUTH_SUCCESS"
    AUTHENTICATION_FAILURE = "AUTH_FAILURE"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    CONFIGURATION_CHANGE = "CONFIG_CHANGE"
    ENCRYPTION_KEY_ROTATION = "KEY_ROTATION"
    SECURITY_VIOLATION = "SECURITY_VIOLATION"


@dataclass
class SecurityContext:
    user_id: str
    tenant_id: str
    session_token: str
    permissions: List[str] = field(default_factory=list)
    clearance_level: SecurityLevel = SecurityLevel.PUBLIC
    request_id: str = field(default_factory=lambda: secrets.token_hex(16))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def is_authorized(self, required_permission: str) -> bool:
        return required_permission in self.permissions
    
    def can_access_level(self, level: SecurityLevel) -> bool:
        return self.clearance_level.value >= level.value


class SecureLogger:
    def __init__(self, name: str, log_file: Optional[str] = None, 
                 min_level: int = logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(min_level)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        if log_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, maxBytes=10485760, backupCount=10
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        self.audit_logger = logging.getLogger(f"{name}.audit")
        self.audit_logger.setLevel(logging.INFO)
        
        if log_file:
            audit_handler = logging.handlers.RotatingFileHandler(
                f"{log_file}.audit", maxBytes=10485760, backupCount=20
            )
            audit_handler.setFormatter(formatter)
            self.audit_logger.addHandler(audit_handler)
    
    def log_sanitized(self, level: int, message: str, context: Optional[SecurityContext] = None):
        sanitized = self._sanitize_message(message)
        if context:
            sanitized = f"[{context.request_id}] {sanitized}"
        self.logger.log(level, sanitized)
    
    def audit(self, event_type: AuditEventType, context: SecurityContext, 
              details: Dict[str, Any], success: bool = True):
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type.value,
            "user_id": context.user_id,
            "tenant_id": context.tenant_id,
            "request_id": context.request_id,
            "success": success,
            "details": self._sanitize_dict(details)
        }
        self.audit_logger.info(json.dumps(audit_entry))
    
    @staticmethod
    def _sanitize_message(message: str) -> str:
        sensitive_patterns = [
            r'password["\']?\s*[:=]\s*["\']?[^"\']+["\']?',
            r'token["\']?\s*[:=]\s*["\']?[^"\']+["\']?',
            r'key["\']?\s*[:=]\s*["\']?[^"\']+["\']?',
            r'secret["\']?\s*[:=]\s*["\']?[^"\']+["\']?',
        ]
        sanitized = message
        for pattern in sensitive_patterns:
            sanitized = __import__('re').sub(pattern, '[REDACTED]', sanitized, flags=__import__('re').IGNORECASE)
        return sanitized
    
    @staticmethod
    def _sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        sensitive_keys = {'password', 'token', 'key', 'secret', 'api_key', 'private_key'}
        sanitized = {}
        for k, v in data.items():
            if k.lower() in sensitive_keys:
                sanitized[k] = '[REDACTED]'
            elif isinstance(v, dict):
                sanitized[k] = SecureLogger._sanitize_dict(v)
            else:
                sanitized[k] = v
        return sanitized


class InputValidator:
    MAX_STRING_LENGTH = 10000
    MAX_ARRAY_LENGTH = 100000
    MAX_TENSOR_SIZE = 1000000000
    
    @staticmethod
    def validate_string(value: Any, max_length: int = MAX_STRING_LENGTH, 
                       pattern: Optional[str] = None) -> str:
        if not isinstance(value, str):
            raise ValueError(f"Expected string, got {type(value)}")
        
        if len(value) > max_length:
            raise ValueError(f"String length {len(value)} exceeds maximum {max_length}")
        
        if pattern:
            import re
            if not re.match(pattern, value):
                raise ValueError(f"String does not match required pattern")
        
        return value
    
    @staticmethod
    def validate_tensor(data: np.ndarray, max_size: int = MAX_TENSOR_SIZE,
                       allowed_dtypes: Optional[List] = None) -> np.ndarray:
        if not isinstance(data, np.ndarray):
            raise ValueError(f"Expected numpy array, got {type(data)}")
        
        if data.size > max_size:
            raise ValueError(f"Tensor size {data.size} exceeds maximum {max_size}")
        
        if allowed_dtypes and data.dtype not in allowed_dtypes:
            raise ValueError(f"Dtype {data.dtype} not in allowed types: {allowed_dtypes}")
        
        return data
    
    @staticmethod
    def validate_integer(value: Any, min_val: int = 0, max_val: int = 2**31 - 1) -> int:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"Expected integer, got {type(value)}")
        
        if not (min_val <= value <= max_val):
            raise ValueError(f"Value {value} outside range [{min_val}, {max_val}]")
        
        return value
    
    @staticmethod
    def validate_float(value: Any, min_val: float = -1e9, max_val: float = 1e9) -> float:
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"Expected float, got {type(value)}")
        
        if not (min_val <= value <= max_val):
            raise ValueError(f"Value {value} outside range [{min_val}, {max_val}]")
        
        return float(value)
    
    @staticmethod
    def validate_list(value: Any, max_length: int = MAX_ARRAY_LENGTH,
                     element_validator: Optional[callable] = None) -> List:
        if not isinstance(value, list):
            raise ValueError(f"Expected list, got {type(value)}")
        
        if len(value) > max_length:
            raise ValueError(f"List length {len(value)} exceeds maximum {max_length}")
        
        if element_validator:
            return [element_validator(item) for item in value]
        
        return value


class EncryptionManager:
    def __init__(self, master_key: Optional[bytes] = None, key_rotation_days: int = 90):
        self.key_rotation_days = key_rotation_days
        self.master_key = master_key or self._generate_master_key()
        self.encryption_keys: Dict[str, Tuple[Fernet, datetime]] = {}
        self.lock = threading.RLock()
    
    def _generate_master_key(self) -> bytes:
        return Fernet.generate_key()
    
    def _derive_key(self, salt: bytes, iterations: int = 100000) -> bytes:
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(self.master_key))
    
    def encrypt_data(self, data: bytes, key_id: str = "default") -> Tuple[bytes, bytes]:
        with self.lock:
            salt = secrets.token_bytes(16)
            derived_key = self._derive_key(salt)
            cipher = Fernet(derived_key)
            
            encrypted = cipher.encrypt(data)
            return salt + encrypted, salt
    
    def decrypt_data(self, encrypted_data: bytes, salt: bytes) -> bytes:
        try:
            derived_key = self._derive_key(salt)
            cipher = Fernet(derived_key)
            return cipher.decrypt(encrypted_data[len(salt):])
        except InvalidToken:
            raise SecurityException("Decryption failed: invalid token or corrupted data")
    
    def generate_hmac(self, data: bytes) -> bytes:
        return hmac.new(self.master_key, data, hashlib.sha256).digest()
    
    def verify_hmac(self, data: bytes, signature: bytes) -> bool:
        expected = self.generate_hmac(data)
        return hmac.compare_digest(expected, signature)
    
    def rotate_keys(self) -> bool:
        with self.lock:
            for key_id, (cipher, created_at) in list(self.encryption_keys.items()):
                age = datetime.utcnow() - created_at
                if age.days > self.key_rotation_days:
                    del self.encryption_keys[key_id]
                    return True
        return False


class SecurityException(Exception):
    pass


class AccessControlManager:
    def __init__(self, threat_model: ThreatModel = ThreatModel.MULTI_TENANT_ISOLATED):
        self.threat_model = threat_model
        self.rbac_policies: Dict[str, List[str]] = {}
        self.tenant_isolation: Dict[str, set] = {}
        self.lock = threading.RLock()
    
    def grant_permission(self, role: str, permission: str):
        with self.lock:
            if role not in self.rbac_policies:
                self.rbac_policies[role] = []
            if permission not in self.rbac_policies[role]:
                self.rbac_policies[role].append(permission)
    
    def check_permission(self, context: SecurityContext, permission: str) -> bool:
        if not context.is_authorized(permission):
            return False
        
        if self.threat_model == ThreatModel.MULTI_TENANT_ISOLATED:
            return self._check_tenant_isolation(context)
        
        return True
    
    def _check_tenant_isolation(self, context: SecurityContext) -> bool:
        with self.lock:
            if context.tenant_id in self.tenant_isolation:
                return context.user_id in self.tenant_isolation[context.tenant_id]
        return False
    
    def register_tenant_user(self, tenant_id: str, user_id: str):
        with self.lock:
            if tenant_id not in self.tenant_isolation:
                self.tenant_isolation[tenant_id] = set()
            self.tenant_isolation[tenant_id].add(user_id)
    
    def enforce_access(self, context: SecurityContext, permission: str):
        if not self.check_permission(context, permission):
            raise SecurityException(f"Access denied: {permission}")


class AuditTrail:
    def __init__(self, db_path: str = "audit.db"):
        self.db_path = db_path
        self.lock = threading.RLock()
        self._init_database()
    
    def _init_database(self):
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute()
                conn.execute()
                conn.execute()
                conn.execute()
                conn.commit()
    
    def record_event(self, event_type: AuditEventType, context: SecurityContext,
                    details: Dict[str, Any], success: bool = True):
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(, (
                    datetime.utcnow().isoformat(),
                    event_type.value,
                    context.user_id,
                    context.tenant_id,
                    context.request_id,
                    success,
                    json.dumps(details)
                ))
                conn.commit()
    
    def query_events(self, user_id: Optional[str] = None, 
                    tenant_id: Optional[str] = None,
                    start_time: Optional[datetime] = None,
                    end_time: Optional[datetime] = None) -> List[Dict]:
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                
                query = "SELECT * FROM audit_events WHERE 1=1"
                params = []
                
                if user_id:
                    query += " AND user_id = ?"
                    params.append(user_id)
                
                if tenant_id:
                    query += " AND tenant_id = ?"
                    params.append(tenant_id)
                
                if start_time: