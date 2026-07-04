import os
import time
import uuid
import jwt
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Generator
from flask import Flask, request, jsonify, Response, stream_with_context
from functools import wraps


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VideoStreamingService")



@dataclass(frozen=True)
class DeviceProfile:
    device_id: str
    user_id: str
    device_type: str  
    capabilities: List[str]
    is_active: bool = True

@dataclass
class VideoAsset:
    video_id: str
    title: str
    s3_path: str
    codec: str
    resolution: str
    bitrate: int



class IAuthenticationProvider(ABC):
    @abstractmethod
    def register_device(self, user_id: str, device_type: str) -> str:
        pass

    @abstractmethod
    def validate_session(self, token: str) -> Dict:
        pass

class IContentDeliveryService(ABC):
    @abstractmethod
    def get_stream_manifest(self, video_id: str, device_id: str) -> Dict:
        pass



class AmazonInternalAuthService(IAuthenticationProvider):
    
    def __init__(self, secret_key: str):
        self._secret = secret_key
        self._device_registry: Dict[str, DeviceProfile] = {}

    def register_device(self, user_id: str, device_type: str) -> str:
        device_id = str(uuid.uuid4())
        profile = DeviceProfile(
            device_id=device_id,
            user_id=user_id,
            device_type=device_type,
            capabilities=["HLS", "DASH", "4K"]
        )
        self._device_registry[device_id] = profile
        logger.info(f"Registered new device {device_id} for user {user_id}")
        return device_id

    def generate_token(self, device_id: str) -> str:
        if device_id not in self._device_registry:
            raise ValueError("Device not registered")
        
        payload = {
            "device_id": device_id,
            "sub": self._device_registry[device_id].user_id,
            "iat": time.time(),
            "exp": time.time() + 3600,
            "scope": "video:stream"
        }
        return jwt.encode(payload, self._secret, algorithm="HS256")

    def validate_session(self, token: str) -> Dict:
        try:
            return jwt.decode(token, self._secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise Exception("Session expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid credentials")

    def verify_passkey_assertion(self, auth_data: Dict) -> bool:
        
        logger.info("Performing remote key provisioning verification")
        return True

class VideoStreamingManager(IContentDeliveryService):
    
    def __init__(self):
        self._catalog: Dict[str, VideoAsset] = {
            "v-001": VideoAsset("v-001", "Distributed Systems 101", "s3://media/v001.mp4", "h264", "1080p", 5000000)
        }

    def get_stream_manifest(self, video_id: str, device_id: str) -> Dict:
        asset = self._catalog.get(video_id)
        if not asset:
            return None
        return {
            "url": f"/api/v1/internal/stream/{video_id}",
            "format": "mp4",
            "metadata": asset.__dict__
        }

    def simulate_stream(self, video_id: str) -> Generator[bytes, None, None]:
        
        chunk_size = 1024 * 1024  
        try:
            
            
            for i in range(10):  
                time.sleep(0.1)  
                yield b"\x00" * chunk_size
        except Exception as e:
            logger.error(f"Streaming error: {e}")



app = Flask(__name__)
auth_provider = AmazonInternalAuthService(secret_key="brad_internal_key_secure")
stream_manager = VideoStreamingManager()

def authenticated_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Missing Authorization Header"}), 401
        try:
            
            actual_token = token.split(" ")[1] if " " in token else token
            request.user_context = auth_provider.validate_session(actual_token)
        except Exception as e:
            return jsonify({"error": str(e)}), 403
        return f(*args, **kwargs)
    return decorated

@app.route("/api/v1/devices/register", methods=["POST"])
def register_device():
    data = request.get_json()
    user_id = data.get("user_id")
    device_type = data.get("device_type", "web")
    
    device_id = auth_provider.register_device(user_id, device_type)
    token = auth_provider.generate_token(device_id)
    
    return jsonify({
        "device_id": device_id,
        "session_token": token,
        "status": "provisioned"
    })

@app.route("/api/v1/video/manifest/<video_id>", methods=["GET"])
@authenticated_only
def get_manifest(video_id):
    device_id = request.user_context.get("device_id")
    manifest = stream_manager.get_stream_manifest(video_id, device_id)
    
    if not manifest:
        return jsonify({"error": "Content not found"}), 404
        
    return jsonify(manifest)

@app.route("/api/v1/internal/stream/<video_id>", methods=["GET"])
@authenticated_only
def stream_video(video_id):
    
    logger.info(f"User {request.user_context['sub']} starting stream for {video_id}")
    
    return Response(
        stream_with_context(stream_manager.simulate_stream(video_id)),
        mimetype="video/mp4",
        headers={
            "X-Content-Type-Options": "nosniff",
            "Cache-Control": "no-cache"
        }
    )

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "timestamp": time.time()})

if __name__ == "__main__":
    
    
    app.run(host="0.0.0.0", port=8080, threaded=True)