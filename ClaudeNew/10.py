import os
import json
import hashlib
import secrets
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from functools import wraps
import logging
from abc import ABC, abstractmethod
import threading
import queue
from collections import defaultdict
import base64
import uuid

import jwt
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import requests
from functools import lru_cache

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SecurityLevel(Enum):
    PUBLIC = "public"
    AUTHENTICATED = "authenticated"
    ADMIN = "admin"
    SYSTEM = "system"


class AuditAction(Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    CONTENT_ACCESS = "CONTENT_ACCESS"
    CONTENT_DOWNLOAD = "CONTENT_DOWNLOAD"
    TOKEN_REFRESH = "TOKEN_REFRESH"
    MFA_CHALLENGE = "MFA_CHALLENGE"
    MFA_SUCCESS = "MFA_SUCCESS"
    MFA_FAILURE = "MFA_FAILURE"
    CREDENTIAL_REVOKE = "CREDENTIAL_REVOKE"
    PERMISSION_CHANGE = "PERMISSION_CHANGE"
    DATA_EXPORT = "DATA_EXPORT"
    PII_ACCESS = "PII_ACCESS"


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    REVOCATION = "revocation"


@dataclass
class SecurityContext:
    user_id: str
    username: str
    roles: List[str]
    mfa_verified: bool
    token_id: str
    issued_at: datetime
    expires_at: datetime
    permissions: List[str]
    device_id: Optional[str] = None
    ip_address: Optional[str] = None


@dataclass
class AuditLog:
    audit_id: str
    user_id: str
    action: str
    resource: str
    timestamp: datetime
    ip_address: str
    success: bool
    details: Dict[str, Any]
    pii_involved: bool = False

    def to_dict(self):
        return {
            'audit_id': self.audit_id,
            'user_id': self.user_id,
            'action': self.action,
            'resource': self.resource,
            'timestamp': self.timestamp.isoformat(),
            'ip_address': self.ip_address,
            'success': self.success,
            'details': self.details,
            'pii_involved': self.pii_involved
        }


class KeyManagementService:
    def __init__(self):
        self._master_key = os.getenv('MASTER_KEY', Fernet.generate_key())
        self._cipher = Fernet(self._master_key)
        self._key_cache: Dict[str, bytes] = {}
        self._rotation_interval = timedelta(days=90)
        self._last_rotation = datetime.utcnow()

    def encrypt_data(self, data: str, key_id: Optional[str] = None) -> str:
        try:
            if isinstance(data, str):
                data = data.encode()
            encrypted = self._cipher.encrypt(data)
            return base64.b64encode(encrypted).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise

    def decrypt_data(self, encrypted_data: str) -> str:
        try:
            encrypted = base64.b64decode(encrypted_data.encode())
            decrypted = self._cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise

    def generate_data_key(self) -> Tuple[str, str]:
        plaintext_key = Fernet.generate_key()
        encrypted_key = self.encrypt_data(plaintext_key.decode())
        return plaintext_key.decode(), encrypted_key

    def should_rotate_keys(self) -> bool:
        return datetime.utcnow() - self._last_rotation > self._rotation_interval

    def rotate_master_key(self) -> None:
        try:
            old_cipher = self._cipher
            self._master_key = Fernet.generate_key()
            self._cipher = Fernet(self._master_key)
            self._last_rotation = datetime.utcnow()
            logger.info("Master key rotated successfully")
        except Exception as e:
            logger.error(f"Key rotation failed: {str(e)}")
            raise


class CredentialManager:
    def __init__(self, kms: KeyManagementService):
        self.kms = kms
        self._credentials: Dict[str, Dict[str, Any]] = {}
        self._revoked_credentials: set = set()
        self._credential_history: List[Dict[str, Any]] = []

    def hash_password(self, password: str) -> str:
        if len(password) < 12:
            raise ValueError("Password must be at least 12 characters long")
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode(), salt).decode()

    def verify_password(self, password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except Exception as e:
            logger.error(f"Password verification failed: {str(e)}")
            return False

    def store_credential(self, user_id: str, credential_type: str, credential_value: str, metadata: Optional[Dict] = None) -> str:
        try:
            credential_id = str(uuid.uuid4())
            encrypted_value = self.kms.encrypt_data(credential_value)

            self._credentials[credential_id] = {
                'user_id': user_id,
                'type': credential_type,
                'value': encrypted_value,
                'created_at': datetime.utcnow(),
                'last_used': None,
                'metadata': metadata or {},
                'is_active': True
            }

            self._credential_history.append({
                'credential_id': credential_id,
                'action': 'CREATE',
                'timestamp': datetime.utcnow(),
                'user_id': user_id
            })

            return credential_id
        except Exception as e:
            logger.error(f"Credential storage failed: {str(e)}")
            raise

    def retrieve_credential(self, credential_id: str) -> Optional[str]:
        if credential_id in self._revoked_credentials:
            logger.warning(f"Attempted access to revoked credential: {credential_id}")
            return None

        if credential_id not in self._credentials:
            return None

        try:
            cred = self._credentials[credential_id]
            cred['last_used'] = datetime.utcnow()
            return self.kms.decrypt_data(cred['value'])
        except Exception as e:
            logger.error(f"Credential retrieval failed: {str(e)}")
            return None

    def revoke_credential(self, credential_id: str, user_id: str, reason: str) -> bool:
        try:
            if credential_id in self._credentials:
                self._revoked_credentials.add(credential_id)
                self._credential_history.append({
                    'credential_id': credential_id,
                    'action': 'REVOKE',
                    'timestamp': datetime.utcnow(),
                    'user_id': user_id,
                    'reason': reason
                })
                logger.info(f"Credential {credential_id} revoked for user {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Credential revocation failed: {str(e)}")
            return False

    def rotate_user_credentials(self, user_id: str) -> List[str]:
        revoked = []
        try:
            for cred_id, cred in self._credentials.items():
                if cred['user_id'] == user_id and cred['is_active']:
                    self.revoke_credential(cred_id, user_id, "Credential rotation")
                    revoked.append(cred_id)
            return revoked
        except Exception as e:
            logger.error(f"Credential rotation failed: {str(e)}")
            return revoked


class TokenManager:
    def __init__(self, kms: KeyManagementService, credential_manager: CredentialManager):
        self.kms = kms
        self.credential_manager = credential_manager
        self._secret_key = os.getenv('JWT_SECRET_KEY', secrets.token_urlsafe(32))
        self._revoked_tokens: Dict[str, datetime] = {}
        self._token_blacklist: set = set()
        self._algorithm = 'HS256'
        self._access_token_expiry = timedelta(minutes=15)
        self._refresh_token_expiry = timedelta(days=7)

    def generate_tokens(self, user_id: str, username: str, roles: List[str], permissions: List[str]) -> Tuple[str, str]:
        try:
            token_id = str(uuid.uuid4())
            now = datetime.utcnow()

            access_payload = {
                'sub': user_id,
                'username': username,
                'roles': roles,
                'permissions': permissions,
                'token_id': token_id,
                'token_type': TokenType.ACCESS.value,
                'iat': now,
                'exp': now + self._access_token_expiry,
                'jti': str(uuid.uuid4())
            }

            refresh_payload = {
                'sub': user_id,
                'username': username,
                'token_id': token_id,
                'token_type': TokenType.REFRESH.value,
                'iat': now,
                'exp': now + self._refresh_token_expiry,
                'jti': str(uuid.uuid4())
            }

            access_token = jwt.encode(access_payload, self._secret_key, algorithm=self._algorithm)
            refresh_token = jwt.encode(refresh_payload, self._secret_key, algorithm=self._algorithm)

            self.credential_manager.store_credential(
                user_id,
                'refresh_token',
                refresh_token,
                {'token_id': token_id, 'access_token_jti': access_payload['jti']}
            )

            logger.info(f"Tokens generated for user {user_id}")
            return access_token, refresh_token
        except Exception as e:
            logger.error(f"Token generation failed: {str(e)}")
            raise

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            if token in self._token_blacklist:
                logger.warning("Token access attempted on blacklisted token")
                return None

            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

            if payload.get('jti') in self._revoked_tokens:
                logger.warning(f"Token access attempted on revoked token: {payload['jti']}")
                return None

            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Expired token presented")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return None

    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        try:
            payload = self.verify_token(refresh_token)
            if not payload or payload.get('token_type') != TokenType.REFRESH.value:
                return None

            user_id = payload['sub']
            username = payload['username']

            new_access_payload = {
                'sub': user_id,
                'username': username,
                'token_type': TokenType.ACCESS.value,
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + self._access_token_expiry,
                'jti': str(uuid.uuid4()),
                'parent_jti': payload.get('jti')
            }

            new_access_token = jwt.encode(new_access_payload, self._secret_key, algorithm=self._algorithm)
            logger.info(f"Access token refreshed for user {user_id}")
            return new_access_token
        except Exception as e:
            logger.error(f"Token refresh failed: {str(e)}")
            return None

    def revoke_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm], options={"verify_exp": False})
            jti = payload.get('jti')
            if jti:
                self._revoked_tokens[jti] = datetime.utcnow() + timedelta(days=7)
                self._token_blacklist.add(token)
                logger.info(f"Token revoked: {jti}")
                return True
            return False
        except Exception as e:
            logger.error(f"Token revocation failed: {str(e)}")
            return False

    def cleanup_expired_revocations(self) -> None:
        now = datetime.utcnow()
        expired = [jti for jti, exp_time in self._revoked_tokens.items() if exp_time < now]
        for jti in expired:
            del self._revoked_tokens[jti]
        logger.info(f"Cleaned up {len(expired)} expired revocations")


class MFAManager:
    def __init__(self, kms: KeyManagementService):
        self.kms = kms
        self._mfa_secrets: Dict[str, Dict[str, Any]] = {}
        self._mfa_attempts: Dict[str, List[Tuple[datetime, bool]]] = defaultdict(list)
        self._lockout_threshold = 5
        self._lockout_duration = timedelta(minutes=15)

    def generate_mfa_secret(self, user_id: str) -> str:
        try:
            secret = base64.b32encode(secrets.token_bytes(32)).decode()
            encrypted_secret = self.kms.encrypt_data(secret)

            self._mfa_secrets[user_id] = {
                'secret': encrypted_secret,
                'created_at': datetime.utcnow(),
                'backup_codes': self._generate_backup_codes(user_id),
                'verified': False
            }

            logger.info(f"MFA secret generated for user {user_id}")
            return secret
        except Exception as e:
            logger.error(f"MFA secret generation failed: {str(e)}")
            raise

    def _generate_backup_codes(self, user_id: str) -> List[str]:
        backup_codes = [secrets.token_hex(4) for _ in range(10)]
        encrypted_codes = [self.kms.encrypt_data(code) for code in backup_codes]
        return encrypted_codes

    def verify_mfa(self, user_id: str, code: str) -> bool:
        try:
            if self._is_locked_out(user_id):
                logger.warning(f"MFA verification attempt while locked out for user {user_id}")
                return False

            if user_id not in self._mfa_secrets:
                return False

            success = self._verify_totp(user_id, code)

            self._mfa_attempts[user_id].append((datetime.utcnow(), success))

            if not success and self._get_failed_attempts(user_id) >= self._lockout_threshold:
                logger.warning(f"MFA lockout triggered for user {user_id}")

            return success
        except Exception as e:
            logger.error