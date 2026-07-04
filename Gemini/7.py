import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey, DateTime, Enum as SQLEnum, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class OrderStatus(Enum):
    PENDING = "PENDING"
    AWAITING_PAYMENT = "AWAITING_PAYMENT"
    FULFILLED = "FULFILLED"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"

class CredentialType(Enum):
    PASSKEY = "PASSKEY"
    REMOTE_KEY = "REMOTE_KEY"
    PASSWORD_HASH = "PASSWORD_HASH"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    account_status = Column(String(50), default="ACTIVE")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    credentials = relationship("SecurityCredential", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user")

class SecurityCredential(Base):
    
    __tablename__ = 'security_credentials'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    credential_type = Column(SQLEnum(CredentialType), nullable=False)
    external_id = Column(String(512), unique=True, nullable=False)  
    public_key = Column(String(2048), nullable=True)
    secret_hash = Column(String(512), nullable=True)
    last_used_at = Column(DateTime)
    
    user = relationship("User", back_populates="credentials")

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sku = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), index=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    version = Column(Integer, default=1)  
    
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    status = Column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float, nullable=False, default=0.0)
    shipping_address = Column(String(512))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey('orders.id'), nullable=False)
    product_id = Column(String(36), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class InventoryException(Exception):
    pass

class BicycleShopDatabase:
    def __init__(self, connection_string: str = "sqlite:///:memory:"):
        self.engine = create_engine(connection_string, echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

class OrderService:
    
    def __init__(self, db: BicycleShopDatabase):
        self.db = db

    def create_user_with_passkey(self, email: str, passkey_id: str, public_key: str) -> str:
        with self.db.get_session() as session:
            user = User(email=email)
            credential = SecurityCredential(
                user=user,
                credential_type=CredentialType.PASSKEY,
                external_id=passkey_id,
                public_key=public_key
            )
            session.add(user)
            session.add(credential)
            session.commit()
            return user.id

    def add_inventory(self, sku: str, name: str, category: str, price: float, quantity: int):
        with self.db.get_session() as session:
            product = Product(sku=sku, name=name, category=category, price=price, stock_quantity=quantity)
            session.add(product)
            session.commit()

    def place_order(self, user_id: str, items_requested: List[Dict[str, Any]]) -> str:
        
        session = self.db.get_session()
        try:
            total = 0.0
            order = Order(user_id=user_id, status=OrderStatus.PENDING)
            session.add(order)
            
            for item in items_requested:
                
                product = session.query(Product).filter_by(id=item['product_id']).with_for_update().one()
                
                if product.stock_quantity < item['quantity']:
                    raise InventoryException(f"Insufficient stock for SKU: {product.sku}")
                
                
                product.stock_quantity -= item['quantity']
                
                
                line_item = OrderItem(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    unit_price=product.price
                )
                total += (product.price * item['quantity'])
                session.add(line_item)
            
            order.total_amount = total
            session.commit()
            return order.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_user_order_history(self, user_id: str):
        with self.db.get_session() as session:
            return session.query(Order).options(joinedload(Order.items)).filter_by(user_id=user_id).all()

if __name__ == "__main__":
    
    shop_db = BicycleShopDatabase("sqlite:///:memory:")
    service = OrderService(shop_db)
    
    
    uid = service.create_user_with_passkey(
        "brad_engineer@amazon.com", 
        "pk_id_992834", 
        "MCowBQYDK2VwAyEAGbSu0DUR6Z8yB58Z3j9p..."
    )
    
    
    service.add_inventory("TRK-DOM-001", "Trek Domane SL 6", "Road", 4200.00, 5)
    service.add_inventory("SPEC-ETH-002", "Specialized Ethos", "Road", 5500.00, 2)
    
    
    with shop_db.get_session() as s:
        bike = s.query(Product).filter_by(sku="TRK-DOM-001").first()
        bike_id = bike.id

    
    try:
        order_id = service.place_order(uid, [{"product_id": bike_id, "quantity": 1}])
        print(f"Order {order_id} placed successfully.")
    except InventoryException as ie:
        print(f"Order failed: {ie}")
    
    
    with shop_db.get_session() as s:
        final_bike = s.query(Product).filter_by(sku="TRK-DOM-001").one()
        print(f"Remaining stock for {final_bike.sku}: {final_bike.stock_quantity}")
        
        user_record = s.query(User).filter_by(id=uid).one()
        print(f"User {user_record.email} has {len(user_record.credentials)} security credentials linked.")