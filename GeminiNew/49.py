import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple, Union
from pydantic import BaseModel, Field, validator, ValidationError
import logging
import hashlib
import hmac
import os
import time
import json


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
)
logger = logging.getLogger("DeviceAnomalyDetectionSystem")

class SecurityConfig:
    
    SECRET_KEY = os.environ.get("DEVICE_METADATA_SALT", "default_secure_salt_change_in_prod").encode()
    MAX_BATCH_SIZE = 1024
    INPUT_DIMENSION = 64  
    ANOMALY_THRESHOLD = 0.15

class DeviceAuthEvent(BaseModel):
    
    device_id: str = Field(..., min_length=16, max_length=128)
    registration_timestamp: int
    firmware_version: str
    ip_address: str
    request_payload_size: int = Field(..., gt=0, lt=1048576) 
    auth_method: str
    metadata_blob: Dict[str, Any]

    @validator('device_id')
    def sanitize_device_id(cls, v):
        
        if not v.isalnum():
            raise ValueError("Device ID must be alphanumeric.")
        return v

class DataSanitizer:
    
    @staticmethod
    def hash_identifier(identifier: str) -> str:
        return hmac.new(
            SecurityConfig.SECRET_KEY, 
            identifier.encode(), 
            hashlib.sha256
        ).hexdigest()

    @staticmethod
    def normalize_features(features: torch.Tensor) -> torch.Tensor:
        
        norm = torch.norm(features, p=2, dim=1, keepdim=True)
        return features / (norm + 1e-8)

class AbstractAnomalyDetector(ABC):
    @abstractmethod
    def train_model(self, data: torch.Tensor):
        pass

    @abstractmethod
    def detect(self, data: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        pass

class DeviceAutoencoder(nn.Module):
    
    def __init__(self, input_dim: int):
        super(DeviceAutoencoder, self).__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(True),
            nn.Dropout(0.1),
            nn.Linear(32, 16),
            nn.ReLU(True),
            nn.Linear(16, 8) 
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(8, 16),
            nn.ReLU(True),
            nn.Linear(16, 32),
            nn.ReLU(True),
            nn.Linear(32, input_dim),
            nn.Sigmoid() 
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.encoder(x)
        x = self.decoder(x)
        return x

class AnomalyInferenceEngine(AbstractAnomalyDetector):
    
    def __init__(self, input_dim: int = SecurityConfig.INPUT_DIMENSION):
        self.model = DeviceAutoencoder(input_dim)
        self.criterion = nn.MSELoss(reduction='none')
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3, weight_decay=1e-5)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def train_model(self, data: torch.Tensor, epochs: int = 50, batch_size: int = 32):
        self.model.train()
        dataset = TensorDataset(data, data)
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        
        for epoch in range(epochs):
            total_loss = 0
            for batch_data, _ in loader:
                batch_data = batch_data.to(self.device)
                self.optimizer.zero_grad()
                output = self.model(batch_data)
                loss = self.criterion(output, batch_data).mean()
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            
            if epoch % 10 == 0:
                logger.info(f"Epoch {epoch} Training Loss: {total_loss/len(loader):.6f}")

    def detect(self, data: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        
        self.model.eval()
        with torch.no_grad():
            data = data.to(self.device)
            reconstructed = self.model(data)
            
            mse_loss = torch.mean(torch.pow(data - reconstructed, 2), dim=1)
            is_anomaly = mse_loss > SecurityConfig.ANOMALY_THRESHOLD
            return is_anomaly, mse_loss

class RemoteKeyProvisioningProtector:
    
    def __init__(self):
        self.engine = AnomalyInferenceEngine()
        self.sanitizer = DataSanitizer()

    def process_registration_event(self, raw_event: Dict[str, Any]) -> Dict[str, Any]:
        try:
            
            event = DeviceAuthEvent(**raw_event)
            
            
            masked_device_id = self.sanitizer.hash_identifier(event.device_id)
            
            
            
            features = self._engineer_features(event)
            
            
            is_anomaly, score = self.engine.detect(features)
            
            result = {
                "device_id_hash": masked_device_id,
                "anomaly_detected": bool(is_anomaly[0].item()),
                "confidence_score": float(score[0].item()),
                "timestamp": time.time(),
                "action": "BLOCK" if is_anomaly[0].item() else "ALLOW"
            }
            
            if result["anomaly_detected"]:
                logger.warning(f"Anomaly detected for device hash {masked_device_id}: Score {result['confidence_score']}")
            
            return result

        except ValidationError as e:
            logger.error(f"Schema validation failed: {e.json()}")
            return {"error": "Invalid Input Schema", "status": 400}
        except Exception as e:
            logger.critical(f"System failure in inference pipeline: {str(e)}")
            return {"error": "Internal Processing Error", "status": 500}

    def _engineer_features(self, event: DeviceAuthEvent) -> torch.Tensor:
        
        
        
        vec = np.zeros(SecurityConfig.INPUT_DIMENSION)
        vec[0] = event.request_payload_size / 1048576.0
        vec[1] = event.registration_timestamp % 86400 / 86400.0 
        
        
        hv = int(hashlib.md5(event.firmware_version.encode()).hexdigest(), 16) % 100
        vec[2] = hv / 100.0
        
        tensor_feat = torch.tensor(vec, dtype=torch.float32).unsqueeze(0)
        return self.sanitizer.normalize_features(tensor_feat)


if __name__ == "__main__":
    
    protector = RemoteKeyProvisioningProtector()
    
    
    logger.info("Initializing model with synthetic baseline...")
    dummy_training_data = torch.randn(100, SecurityConfig.INPUT_DIMENSION)
    protector.engine.train_model(dummy_training_data, epochs=5)

    
    sample_event = {
        "device_id": "AMZN-DEV-99283746551234",
        "registration_timestamp": int(time.time()),
        "firmware_version": "v2.4.1-stable",
        "ip_address": "192.168.1.50",
        "request_payload_size": 2048,
        "auth_method": "RSA_2048_PKI",
        "metadata_blob": {"region": "us-east-1", "retry_count": 0}
    }

    response = protector.process_registration_event(sample_event)
    print(json.dumps(response, indent=2))

    
    malicious_event = {
        "device_id": "ATTACKER_DEVICE_000000000",
        "registration_timestamp": int(time.time()),
        "firmware_version": "v9.9.9-overflow",
        "ip_address": "10.0.0.1",
        "request_payload_size": 999999, 
        "auth_method": "UNKNOWN",
        "metadata_blob": {"debug": True}
    }
    
    malicious_response = protector.process_registration_event(malicious_event)
    print(json.dumps(malicious_response, indent=2))