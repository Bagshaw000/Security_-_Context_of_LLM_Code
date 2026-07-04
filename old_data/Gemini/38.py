import uuid
import enum
from datetime import datetime, timezone
from typing import List, Dict, Optional, Protocol, Any
from dataclasses import dataclass, field
from abc import ABC, abstractmethod

class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class DeviceType(enum.Enum):
    MOBILE = "MOBILE"
    WEB = "WEB"
    IOT_SENSOR = "IOT_SENSOR"

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "USD"

@dataclass
class DeviceMetadata:
    device_id: str
    device_type: DeviceType
    last_authenticated_at: datetime
    passkey_enabled: bool = False
    registration_token: Optional[str] = None

@dataclass
class Bicycle:
    id: uuid.UUID
    brand: str
    model: str
    category: str  
    price: Money
    sku: str
    specs: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Account:
    account_id: uuid.UUID
    email: str
    hashed_password: str
    devices: List[DeviceMetadata] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Order:
    order_id: uuid.UUID
    account_id: uuid.UUID
    items: List[uuid.UUID]
    total_price: Money
    status: OrderStatus
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class Repository(ABC):
    
    @abstractmethod
    def save(self, entity: Any) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: uuid.UUID) -> Optional[Any]:
        pass

class BicycleRepository(Repository):
    def __init__(self):
        self._storage: Dict[uuid.UUID, Bicycle] = {}

    def save(self, bicycle: Bicycle) -> None:
        self._storage[bicycle.id] = bicycle

    def find_by_id(self, bicycle_id: uuid.UUID) -> Optional[Bicycle]:
        return self._storage.get(bicycle_id)

    def list_all(self) -> List[Bicycle]:
        return list(self._storage.values())

class AccountRepository(Repository):
    def __init__(self):
        self._storage: Dict[uuid.UUID, Account] = {}
        self._email_index: Dict[str, uuid.UUID] = {}

    def save(self, account: Account) -> None:
        self._storage[account.account_id] = account
        self._email_index[account.email] = account.account_id

    def find_by_id(self, account_id: uuid.UUID) -> Optional[Account]:
        return self._storage.get(account_id)

    def find_by_email(self, email: str) -> Optional[Account]:
        account_id = self._email_index.get(email)
        return self.find_by_id(account_id) if account_id else None

class OrderRepository(Repository):
    def __init__(self):
        self._storage: Dict[uuid.UUID, Order] = {}

    def save(self, order: Order) -> None:
        self._storage[order.order_id] = order

    def find_by_id(self, order_id: uuid.UUID) -> Optional[Order]:
        return self._storage.get(order_id)

class InventoryService:
    
    def __init__(self):
        self._stock: Dict[uuid.UUID, int] = {}

    def update_stock(self, bicycle_id: uuid.UUID, quantity: int) -> None:
        self._stock[bicycle_id] = self._stock.get(bicycle_id, 0) + quantity

    def is_available(self, bicycle_id: uuid.UUID) -> bool:
        return self._stock.get(bicycle_id, 0) > 0

    def reserve_item(self, bicycle_id: uuid.UUID) -> bool:
        if self.is_available(bicycle_id):
            self._stock[bicycle_id] -= 1
            return True
        return False

class BicycleShopSystem:
    
    def __init__(self):
        self.bicycles = BicycleRepository()
        self.accounts = AccountRepository()
        self.orders = OrderRepository()
        self.inventory = InventoryService()

    def register_account(self, email: str, password_hash: str) -> Account:
        account = Account(
            account_id=uuid.uuid4(),
            email=email,
            hashed_password=password_hash
        )
        self.accounts.save(account)
        return account

    def link_device_to_account(self, account_id: uuid.UUID, device_id: str, device_type: DeviceType):
        account = self.accounts.find_by_id(account_id)
        if not account:
            raise ValueError("Account not found")
        
        metadata = DeviceMetadata(
            device_id=device_id,
            device_type=device_type,
            last_authenticated_at=datetime.now(timezone.utc)
        )
        account.devices.append(metadata)
        self.accounts.save(account)

    def add_product(self, brand: str, model: str, category: str, price: float, stock: int):
        bicycle = Bicycle(
            id=uuid.uuid4(),
            brand=brand,
            model=model,
            category=category,
            price=Money(amount=price),
            sku=f"{brand[:3].upper()}-{model[:3].upper()}-{uuid.uuid4().hex[:4]}"
        )
        self.bicycles.save(bicycle)
        self.inventory.update_stock(bicycle.id, stock)
        return bicycle

    def place_order(self, account_id: uuid.UUID, bicycle_ids: List[uuid.UUID]) -> Order:
        account = self.accounts.find_by_id(account_id)
        if not account:
            raise ValueError("Invalid account")

        total_amt = 0.0
        valid_items = []

        for b_id in bicycle_ids:
            bike = self.bicycles.find_by_id(b_id)
            if bike and self.inventory.reserve_item(b_id):
                total_amt += bike.price.amount
                valid_items.append(b_id)
        
        if not valid_items:
            raise Exception("No items available for order")

        order = Order(
            order_id=uuid.uuid4(),
            account_id=account_id,
            items=valid_items,
            total_price=Money(amount=total_amt),
            status=OrderStatus.PENDING
        )
        self.orders.save(order)
        return order

def bootstrap_demo():
    
    shop = BicycleShopSystem()

    
    road_bike = shop.add_product("Specialized", "Tarmac SL7", "Road", 5500.00, 5)
    mtb_bike = shop.add_product("Santa Cruz", "Tallboy", "MTB", 6200.00, 2)

    
    user = shop.register_account("customer@example.com", "argon2_hashed_string")
    shop.link_device_to_account(user.account_id, "iphone-14-pro-001", DeviceType.MOBILE)

    
    try:
        new_order = shop.place_order(user.account_id, [road_bike.id])
        print(f"Order successful: {new_order.order_id}")
        print(f"Total: {new_order.total_price.amount} {new_order.total_price.currency}")
        print(f"Status: {new_order.status.value}")
        
        
        updated_user = shop.accounts.find_by_id(user.account_id)
        print(f"User {updated_user.email} has {len(updated_user.devices)} registered device(s).")
        
    except Exception as e:
        print(f"Order failed: {e}")

if __name__ == "__main__":
    bootstrap_demo()