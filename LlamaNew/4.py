import hashlib
import hmac
import secrets
import json
import base64
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Union

class SecurityProvider:
    
    
    @staticmethod
    def hash_password(password: str) -> tuple[bytes, bytes]:
        salt = secrets.token_bytes(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 200000)
        return key, salt

    @staticmethod
    def verify_password(stored_hash: bytes, salt: bytes, provided_password: str) -> bool:
        new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 200000)
        return hmac.compare_digest(stored_hash, new_hash)

    @staticmethod
    def generate_session_token() -> str:
        return secrets.token_urlsafe(64)

    @staticmethod
    def sanitize(text: str) -> str:
        
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&

    @staticmethod
    def encrypt_payload(data: str, master_key: bytes) -> str:
        
        nonce = secrets.token_bytes(12)
        
        encoded_data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        auth_tag = hmac.new(master_key, (nonce.hex() + encoded_data).encode(), hashlib.sha256).hexdigest()
        return f"{nonce.hex()}:{auth_tag}:{encoded_data}"

    @staticmethod
    def decrypt_payload(encrypted_blob: str, master_key: bytes) -> str:
        try:
            nonce_hex, auth_tag, encoded_data = encrypted_blob.split(":")
            
            expected_tag = hmac.new(master_key, (nonce_hex + encoded_data).encode(), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(expected_tag, auth_tag):
                raise PermissionError("Data integrity check failed.")
            return base64.b64decode(encoded_data).decode('utf-8')
        except Exception:
            return "[DECRYPTION_FAILURE]"

class DeviceMetadata:
    def __init__(self, device_id: str, device_type: str, user_agent: str):
        self.device_id = device_id
        self.device_type = device_type
        self.user_agent = user_agent
        self.registration_date = datetime.utcnow()
        self.is_active = True

class TodoItem:
    def __init__(self, owner_id: str, encrypted_content: str):
        self.id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.content_blob = encrypted_content
        self.created_at = datetime.utcnow()
        self.is_completed = False

class DataStorageInterface(ABC):
    @abstractmethod
    def put_user(self, user_record: Dict): pass
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[Dict]: pass
    @abstractmethod
    def put_todo(self, todo: TodoItem): pass
    @abstractmethod
    def get_user_todos(self, user_id: str) -> List[TodoItem]: pass

class InMemoryScalableStore(DataStorageInterface):
    
    def __init__(self):
        self._users = {} 
        self._todos = {} 
        self._devices = {} 

    def put_user(self, user_record: Dict):
        self._users[user_record['username']] = user_record

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        return self._users.get(username)

    def put_todo(self, todo: TodoItem):
        if todo.owner_id not in self._todos:
            self._todos[todo.owner_id] = []
        self._todos[todo.owner_id].append(todo)

    def get_user_todos(self, user_id: str) -> List[TodoItem]:
        return self._todos.get(user_id, [])

class DeviceManagementSystem:
    
    def __init__(self):
        self.registered_devices = {}

    def register_device(self, user_id: str, device_info: Dict) -> bool:
        device_id = device_info.get('device_id')
        if not device_id: return False
        self.registered_devices[device_id] = {
            "owner": user_id,
            "status": "provisioned",
            "linked_at": datetime.utcnow()
        }
        return True

    def verify_device_link(self, user_id: str, device_id: str) -> bool:
        record = self.registered_devices.get(device_id)
        return record and record['owner'] == user_id

class AmazonTodoService:
    def __init__(self, storage: DataStorageInterface):
        self.storage = storage
        self.dms = DeviceManagementSystem()
        self.active_sessions = {} 
        self._master_key = secrets.token_bytes(32) 

    def create_account(self, username: str, password: str) -> Dict:
        if self.storage.get_user_by_username(username):
            return {"status": "error", "message": "Identity already exists."}
        
        
        clean_username = SecurityProvider.sanitize(username)
        pw_hash, salt = SecurityProvider.hash_password(password)
        
        user_id = str(uuid.uuid4())
        user_record = {
            "user_id": user_id,
            "username": clean_username,
            "auth_material": {"hash": pw_hash, "salt": salt},
            "created_at": datetime.utcnow()
        }
        self.storage.put_user(user_record)
        return {"status": "success", "user_id": user_id}

    def login(self, username: str, password: str, device_id: str, device_type: str) -> Optional[str]:
        user = self.storage.get_user_by_username(username)
        if not user:
            return None
        
        valid = SecurityProvider.verify_password(
            user['auth_material']['hash'], 
            user['auth_material']['salt'], 
            password
        )
        
        if valid:
            
            self.dms.register_device(user['user_id'], {"device_id": device_id, "type": device_type})
            
            
            token = SecurityProvider.generate_session_token()
            self.active_sessions[token] = {
                "user_id": user['user_id'],
                "device_id": device_id,
                "expiry": datetime.utcnow() + timedelta(hours=2)
            }
            return token
        return None

    def add_todo(self, token: str, content: str) -> Dict:
        session = self._get_valid_session(token)
        if not session:
            return {"status": "unauthorized"}

        
        safe_content = SecurityProvider.sanitize(content)
        encrypted_content = SecurityProvider.encrypt_payload(safe_content, self._master_key)
        
        new_todo = TodoItem(session['user_id'], encrypted_content)
        self.storage.put_todo(new_todo)
        return {"status": "success", "todo_id": new_todo.id}

    def fetch_todos(self, token: str) -> List[Dict]:
        session = self._get_valid_session(token)
        if not session:
            return []

        raw_items = self.storage.get_user_todos(session['user_id'])
        results = []
        for item in raw_items:
            results.append({
                "id": item.id,
                "content": SecurityProvider.decrypt_payload(item.content_blob, self._master_key),
                "timestamp": item.created_at.isoformat()
            })
        return results

    def provision_passkey(self, token: str) -> Dict:
        
        session = self._get_valid_session(token)
        if not session:
            return {"status": "unauthorized"}
        
        
        passkey_id = f"pk_{secrets.token_hex(16)}"
        return {
            "status": "success", 
            "passkey_id": passkey_id, 
            "mechanism": "WebAuthn_Mock",
            "device_bound": session['device_id']
        }

    def _get_valid_session(self, token: str) -> Optional[Dict]:
        session = self.active_sessions.get(token)
        if not session:
            return None
        if datetime.utcnow() > session['expiry']:
            del self.active_sessions[token]
            return None
        return session

if __name__ == "__main__":
    
    storage_engine = InMemoryScalableStore()
    app_service = AmazonTodoService(storage_engine)

    
    print("--- Registering User ---")
    reg_response = app_service.create_account("b_engineer@amazon.com", "CorrectHorseBatteryStaple123!")
    print(f"Registration: {reg_response['status']}")

    
    print("\n--- Authenticating Device ---")
    device_uuid = "DMS-7744-9900-X"
    auth_token = app_service.login("b_engineer@amazon.com", "CorrectHorseBatteryStaple123!", device_uuid, "Workstation")
    
    if auth_token:
        print(f"Session established. Token: {auth_token[:12]}...")

        
        app_service.add_todo(auth_token, "Review Passkey architectural design docs")
        app_service.add_todo(auth_token, "Fix XSS vulnerability in legacy portal <script>alert(1)</script>")
        
        
        print("\n--- Retrieving Encrypted Todo List ---")
        my_todos = app_service.fetch_todos(auth_token)
        for t in my_todos:
            print(f"ID: {t['id'][:8]} | Content: {t['content']}")

        
        print("\n--- Provisioning Remote Passkey ---")
        pk_info = app_service.provision_passkey(auth_token)
        print(f"Passkey Status: {pk_info['status']} | KeyID: {pk_info['passkey_id']}")
    else:
        print("Authentication failed.")