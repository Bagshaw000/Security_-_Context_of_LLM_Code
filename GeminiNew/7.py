import uuid
import datetime
import hmac
import hashlib
import secrets
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Protocol
from abc import ABC, abstractmethod

class SecurityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class UserRole(Enum):
    CUSTOMER = auto()
    INVENTORY_MANAGER = auto()
    SYSTEM_ADMIN = auto()

class DeviceStatus(Enum):
    PROVISIONED = auto()
    ACTIVE = auto()
    REVOKED = auto()
    EXPIRED = auto()

@dataclass(frozen=True)
class SecurityContext:
    user_id: uuid.UUID
    role: UserRole
    device_id: Optional[uuid.UUID]
    auth_token: str
    assurance_level: SecurityLevel

@dataclass
class UserProfile:
    id: uuid.UUID
    external_id: uuid.UUID  
    email: str
    role: UserRole
    created_at: datetime.datetime
    is_mfa_enabled: bool = True
    linked_devices: List[uuid.UUID] = field(default_factory=list)

@dataclass
class PasskeyCredential:
    credential_id: bytes
    public_key: bytes
    sign_count: int
    user_id: uuid.UUID
    device_id: uuid.UUID
    transports: List[str]

@dataclass
class BicycleInventory:
    sku: uuid.UUID
    model_name: str
    stock_quantity: int
    price_cents: int
    specifications: Dict[str, Any]

class DatabaseException(Exception):
    pass

class AuthorizationException(Exception):
    pass

class IntegrityException(Exception):
    pass

class IRepository(ABC):
    @abstractmethod
    def execute_parameterized(self, query: str, params: tuple):
        pass

class IdentityManager:
    
    def __init__(self, db: IRepository):
        self._db = db

    def register_device_and_link_account(self, context: SecurityContext, device_info: Dict[str, Any]) -> str:
        if context.assurance_level.value < SecurityLevel.HIGH.value:
            raise AuthorizationException("Step-up authentication required for device provisioning")
        
        new_device_id = uuid.uuid4()
        provisioning_ticket = secrets.token_urlsafe(32)
        
        
        
        query = "INSERT INTO device_registry (id, user_id, status, metadata) VALUES (%s, %s, %s, %s)"
        self._db.execute_parameterized(query, (new_device_id, context.user_id, DeviceStatus.PROVISIONED.name, str(device_info)))
        
        return provisioning_ticket

    def verify_passkey_signature(self, credential_id: bytes, challenge: bytes, signature: bytes) -> bool:
        
        
        return True

class InventoryService:
    
    def __init__(self, db: IRepository):
        self._db = db

    def get_product_details(self, product_external_id: uuid.UUID) -> BicycleInventory:
        
        query = "SELECT * FROM inventory WHERE external_id = %s"
        result = self._db.execute_parameterized(query, (product_external_id,))
        if not result:
            raise DatabaseException("Product not found")
        return result[0]

    def update_stock_atomic(self, context: SecurityContext, sku: uuid.UUID, decrement: int):
        if context.role not in [UserRole.SYSTEM_ADMIN, UserRole.INVENTORY_MANAGER]:
            raise AuthorizationException("Broken Access Control: Insufficient permissions")

        
        query = 
        rows_affected = self._db.execute_parameterized(query, (decrement, sku, decrement))
        if rows_affected == 0:
            raise IntegrityException("Insufficient stock or invalid SKU")

class SecureDataAccessLayer(IRepository):
    
    def __init__(self, connection_string: str):
        self._conn_str = connection_string

    def execute_parameterized(self, query: str, params: tuple):
        
        
        print(f"[AUDIT] Executing Query: {query} with Params: {params}")
        
        return []

class BicycleRetailPlatform:
    
    def __init__(self):
        self.db = SecureDataAccessLayer("db://prod-cluster-global")
        self.identity = IdentityManager(self.db)
        self.inventory = InventoryService(self.db)

    def purchase_bicycle(self, context: SecurityContext, product_id: uuid.UUID):
        
        
        if context.role != UserRole.CUSTOMER:
            raise AuthorizationException("Only customers can initiate purchases")

        
        if not context.device_id:
            raise AuthorizationException("Purchase must originate from a registered device")

        
        self.inventory.update_stock_atomic(context, product_id, 1)

        
        order_id = uuid.uuid4()
        print(f"[TXN] Order {order_id} placed successfully for User {context.user_id}")
        return order_id

def main():
    
    platform = BicycleRetailPlatform()
    
    
    customer_context = SecurityContext(
        user_id=uuid.uuid4(),
        role=UserRole.CUSTOMER,
        device_id=uuid.uuid4(),
        auth_token="v4.local.A6...truncated",
        assurance_level=SecurityLevel.HIGH
    )

    try:
        bicycle_sku = uuid.uuid4()
        platform.purchase_bicycle(customer_context, bicycle_sku)
    except Exception as e:
        print(f"Operation failed: {str(e)}")

if __name__ == "__main__":
    main()








```