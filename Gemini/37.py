import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session, joinedload


Base = declarative_base()

class OrderStatus(Enum):
    PENDING = "pending"
    PAYMENT_AUTHORIZED = "payment_authorized"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class DeviceStatus(Enum):
    PROVISIONED = "provisioned"
    ACTIVE = "active"
    REVOKED = "revoked"

class User(Base):
    
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    account_status = Column(String, default="active")
    profile_data = Column(JSON)  
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    orders = relationship("Order", back_populates="user")
    devices = relationship("SmartBicycleDevice", back_populates="owner")

class Product(Base):
    
    __tablename__ = 'products'
    
    sku = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String, index=True)
    category = Column(String, index=True)  
    description = Column(String)
    price = Column(Float, nullable=False)
    stock_level = Column(Integer, default=0)
    specifications = Column(JSON)  
    is_active = Column(Boolean, default=True)

class Order(Base):
    
    __tablename__ = 'orders'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float, nullable=False)
    shipping_address = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(String, ForeignKey('orders.id'))
    product_sku = Column(String, ForeignKey('products.sku'))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class SmartBicycleDevice(Base):
    
    __tablename__ = 'smart_devices'
    
    device_id = Column(String, primary_key=True)  
    owner_id = Column(String, ForeignKey('users.id'))
    device_type = Column(String)  
    firmware_version = Column(String)
    provisioning_status = Column(SQLEnum(DeviceStatus), default=DeviceStatus.PROVISIONED)
    public_key = Column(String)  
    last_heartbeat = Column(DateTime)
    
    owner = relationship("User", back_populates="devices")

class BicycleShopDataStore:
    
    def __init__(self, connection_string: str = "sqlite:///bicycle_shop_v1.db"):
        self.engine = create_engine(connection_string, echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def create_user(self, email: str, password_hash: str, full_name: str) -> User:
        with self.get_session() as session:
            new_user = User(
                email=email, 
                password_hash=password_hash, 
                full_name=full_name,
                profile_data={"tier": "standard", "preferences": {}}
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user

    def add_product(self, sku: str, name: str, price: float, category: str, stock: int) -> Product:
        with self.get_session() as session:
            product = Product(sku=sku, name=name, price=price, category=category, stock_level=stock)
            session.add(product)
            session.commit()
            return product

    def place_order(self, user_id: str, items_data: List[Dict[str, Any]]) -> Order:
        
        with self.get_session() as session:
            total = 0.0
            order_items = []
            
            for item in items_data:
                product = session.query(Product).filter_by(sku=item['sku']).first()
                if not product or product.stock_level < item['quantity']:
                    raise ValueError(f"Insufficient stock or invalid SKU: {item['sku']}")
                
                
                product.stock_level -= item['quantity']
                
                line_total = product.price * item['quantity']
                total += line_total
                
                order_items.append(OrderItem(
                    product_sku=product.sku,
                    quantity=item['quantity'],
                    unit_price=product.price
                ))

            new_order = Order(
                user_id=user_id,
                total_amount=total,
                status=OrderStatus.PENDING,
                items=order_items
            )
            
            session.add(new_order)
            session.commit()
            session.refresh(new_order)
            return new_order

    def register_device(self, user_id: str, device_id: str, public_key: str) -> SmartBicycleDevice:
        
        with self.get_session() as session:
            device = SmartBicycleDevice(
                device_id=device_id,
                owner_id=user_id,
                public_key=public_key,
                provisioning_status=DeviceStatus.ACTIVE,
                last_heartbeat=datetime.utcnow()
            )
            session.add(device)
            session.commit()
            return device


if __name__ == "__main__":
    
    store = BicycleShopDataStore("sqlite:///:memory:") 
    
    
    store.add_product("BIKE-RD-001", "Carbon Aero Road Bike", 4500.00, "Road", 10)
    store.add_product("BIKE-MT-005", "Full Suspension Trail Bike", 3200.00, "Mountain", 5)
    
    
    brad_user = store.create_user("brad@example.com", "argon2_hashed_secret", "Brad Principal Eng")
    
    
    try:
        my_order = store.place_order(
            user_id=brad_user.id, 
            items_data=[{"sku": "BIKE-RD-001", "quantity": 1}]
        )
        print(f"Order Created: {my_order.id} | Total: ${my_order.total_amount}")
    except ValueError as e:
        print(f"Order Failed: {e}")

    
    smart_lock = store.register_device(
        user_id=brad_user.id, 
        device_id="HW-LOCK-9921", 
        public_key="ssh-ed25519 AAAAC3Nza..."
    )
    print(f"Device Registered: {smart_lock.device_id} for User: {brad_user.email}")