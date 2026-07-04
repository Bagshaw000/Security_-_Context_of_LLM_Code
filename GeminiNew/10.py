import hmac
import hashlib
import secrets
import time
import json
import base64
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from enum import Enum
from uuid import uuid4



class SecurityException(Exception):
    
    pass

class AuthenticationError(SecurityException):
    
    pass

class AuthorizationError(SecurityException):
    
    pass

class ValidationException(SecurityException):
    
    pass



class DeviceType(Enum):
    SMART_TV = "smart_tv"
    MOBILE = "mobile"
    WEB = "web"
    STREAMING_STICK = "streaming_stick"

@dataclass
class PasskeyCredential:
    credential_id: str
    public_key: bytes
    sign_count: int
    transports: List[str]
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class DeviceProfile:
    device_id: str
    user_id: str
    device_type: DeviceType
    device_name: str
    last_login: datetime
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class UserAccount:
    user_id: str
    email: str
    passkeys: Dict[str, PasskeyCredential] = field(default_factory=dict)
    linked_devices: List[str] = field(default_factory=list)
    is_mfa_enabled: bool = True



class IRepository(ABC):
    
    @abstractmethod
    def get_user(self, user_id: str) -> Optional[UserAccount]: pass
    
    @abstractmethod
    def save_user(self, user: UserAccount) -> None: pass
    
    @abstractmethod
    def get_device(self, device_id: str) -> Optional[DeviceProfile]: pass
    
    @abstractmethod
    def save_device(self, device: DeviceProfile) -> None: pass



class PasskeyService:
    
    def __init__(self, repository: IRepository):
        self.repo = repository
        self.challenge_timeout = 300 
        
        self._challenges: Dict[str, Tuple[str, float]] = {}

    def generate_registration_challenge(self, user_id: str) -> str:
        challenge = secrets.token_urlsafe(32)
        self._challenges[user_id] = (challenge, time.time())
        return challenge

    def verify_registration(self, user_id: str, challenge: str, credential_data: Dict[str, Any]) -> bool:
        
        stored = self._challenges.pop(user_id, None)
        if not stored or not hmac.compare_digest(stored[0], challenge):
            raise AuthenticationError("Invalid or expired challenge")
        
        if time.time() - stored[1] > self.challenge_timeout:
            raise AuthenticationError("Challenge expired")

        
        
        
        
        new_credential = PasskeyCredential(
            credential_id=credential_data['id'],
            public_key=credential_data['public_key'],
            sign_count=0,
            transports=credential_data.get('transports', [])
        )
        
        user = self.repo.get_user(user_id)
        if not user:
            raise ValidationException("User not found")
            
        user.passkeys[new_credential.credential_id] = new_credential
        self.repo.save_user(user)
        return True

class SessionManager:
    
    def __init__(self, secret_key: str):
        self._secret_key = secret_key
        self._algorithm = "HS256"

    def create_session_token(self, user_id: str, device_id: str) -> str:
        
        header = base64.urlsafe_b64encode(json.dumps({"alg": self._algorithm, "typ": "JWT"}).encode()).decode()
        payload_data = {
            "sub": user_id,
            "did": device_id,
            "iat": int(time.time()),
            "exp": int(time.time()) + 3600,
            "jti": str(uuid4())
        }
        payload = base64.urlsafe_b64encode(json.dumps(payload_data).encode()).decode()
        
        signature = self._generate_signature(f"{header}.{payload}")
        return f"{header}.{payload}.{signature}"

    def _generate_signature(self, data: str) -> str:
        return hmac.new(
            self._secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()

    def validate_session(self, token: str) -> Dict[str, Any]:
        try:
            parts = token.split(".")
            if len(parts) != 3:
                raise AuthenticationError("Invalid token format")
            
            header, payload, signature = parts
            expected_signature = self._generate_signature(f"{header}.{payload}")
            
            if not hmac.compare_digest(signature, expected_signature):
                raise AuthenticationError("Invalid token signature")
            
            decoded_payload = json.loads(base64.urlsafe_b64decode(payload + "==").decode())
            
            if decoded_payload['exp'] < time.time():
                raise AuthenticationError("Token expired")
                
            return decoded_payload
        except Exception as e:
            logging.error(f"Token validation failed: {str(e)}")
            raise AuthenticationError("Unauthorized access")



class VideoStreamingBackend:
    
    def __init__(self, repository: IRepository, session_manager: SessionManager):
        self.repository = repository
        self.session_manager = session_manager
        self.passkey_service = PasskeyService(repository)
        self.logger = logging.getLogger("StreamingBackend")

    def register_device(self, user_id: str, device_info: Dict[str, Any]) -> str:
        
        
        required = ['device_type', 'device_name']
        if not all(k in device_info for k in required):
            raise ValidationException("Missing required device metadata")

        user = self.repository.get_user(user_id)
        if not user:
            raise AuthorizationError("Action not permitted for this identity")

        
        device_id = f"dev_{secrets.token_hex(12)}"
        
        new_device = DeviceProfile(
            device_id=device_id,
            user_id=user_id,
            device_type=DeviceType(device_info['device_type']),
            device_name=device_info['device_name'],
            last_login=datetime.utcnow()
        )

        user.linked_devices.append(device_id)
        self.repository.save_device(new_device)
        self.repository.save_user(user)
        
        self.logger.info(f"Device {device_id} successfully linked to user {user_id}")
        return device_id

    def authenticate_with_passkey(self, user_id: str, challenge: str, auth_payload: Dict[str, Any]) -> str:
        
        
        
        is_valid = self.passkey_service.verify_registration(user_id, challenge, auth_payload)
        
        if is_valid:
            
            device_id = auth_payload.get('device_id', 'unknown_web_client')
            return self.session_manager.create_session_token(user_id, device_id)
        
        raise AuthenticationError("Passkey authentication failed")

    def get_content_stream(self, session_token: str, content_id: str) -> Dict[str, str]:
        
        session = self.session_manager.validate_session(session_token)
        user_id = session['sub']
        
        
        user = self.repository.get_user(user_id)
        if not user:
            raise AuthorizationError("User profile inactive")

        
        
        self.logger.info(f"User {user_id} accessing content {content_id}")
        
        return {
            "stream_url": f"https://cdn.streaming-service.com/manifest/{content_id}.m3u8",
            "drm_token": secrets.token_urlsafe(64),
            "expires_at": (datetime.utcnow() + timedelta(hours=2)).isoformat()
        }



class InMemRepository(IRepository):
    def __init__(self):
        self.users: Dict[str, UserAccount] = {}
        self.devices: Dict[str, DeviceProfile] = {}

    def get_user(self, user_id: str) -> Optional[UserAccount]:
        return self.users.get(user_id)

    def save_user(self, user: UserAccount) -> None:
        self.users[user.user_id] = user

    def get_device(self, device_id: str) -> Optional[DeviceProfile]:
        return self.devices.get(device_id)

    def save_device(self, device: DeviceProfile) -> None:
        self.devices[device.device_id] = device



if __name__ == "__main__":
    
    repo = InMemRepository()
    session_mgr = SessionManager(secret_key=secrets.token_hex(32))
    backend = VideoStreamingBackend(repo, session_mgr)

    
    test_user_id = "user_001"
    repo.save_user(UserAccount(user_id=test_user_id, email="brad@amazon.com"))

    
    try:
        device_id = backend.register_device(test_user_id, {
            "device_type": "smart_tv",
            "device_name": "Living Room FireTV"
        })
        print(f"Device Registered: {device_id}")

        
        challenge = backend.passkey_service.generate_registration_challenge(test_user_id)
        
        
        mock_credential = {
            "id": "cred_abc123",
            "public_key": b"mock_pub_key_bytes",
            "transports": ["internal"]
        }
        
        backend.passkey_service.verify_registration(test_user_id, challenge, mock_credential)
        print("Passkey Registered Successfully")

        
        
        login_challenge = backend.passkey_service.generate_registration_challenge(test_user_id)
        session_token = backend.authenticate_with_passkey(
            test_user_id, 
            login_challenge, 
            {"id": "cred_abc123", "public_key": b"mock_pub_key_bytes", "device_id": device_id}
        )
        print(f"Session Established: {session_token[:20]}...")

        
        content = backend.get_content_stream(session_token, "movie_premium_4k_001")
        print(f"Stream URL: {content['stream_url']}")

    except SecurityException as e:
        print(f"Security violation detected: {e}")
    except Exception as e:
        print(f"System error: {e}")