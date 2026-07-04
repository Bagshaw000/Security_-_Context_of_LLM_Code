import uuid
from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, create_engine, Text, Index
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

Base = declarative_base()

class User(Base):
    
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=True)
    
    
    passkey_credential_id = Column(String(512), nullable=True, unique=True)
    public_key = Column(Text, nullable=True)
    sign_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"<User(email='{self.email}', id='{self.id}')>"

class Product(Base):
    
    __tablename__ = 'products'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sku = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100)) 
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    
    __tablename__ = 'orders'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    status = Column(String(50), default="PENDING") 
    total_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    
    __tablename__ = 'order_items'
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey('orders.id'), nullable=False)
    product_id = Column(String(36), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price_at_purchase = Column(Float, nullable=False)
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class BicycleShopDatabase:
    
    def __init__(self, connection_uri: str = "sqlite:///bicycle_shop.db"):
        self.engine = create_engine(connection_uri, pool_pre_ping=True)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)

    def get_session(self) -> Session:
        return self.SessionLocal()

class OrderService:
    
    def __init__(self, db: BicycleShopDatabase):
        self.db = db

    def create_order(self, user_id: str, item_specs: List[Dict]) -> str:
        session = self.db.get_session()
        try:
            new_order = Order(user_id=user_id, status="PENDING")
            total = 0.0
            
            for spec in item_specs:
                product = session.query(Product).filter_by(id=spec['product_id']).with_for_update().first()
                
                if not product:
                    raise ValueError(f"Product {spec['product_id']} not found")
                
                if product.stock_quantity < spec['quantity']:
                    raise ValueError(f"Insufficient stock for {product.name}")
                
                
                product.stock_quantity -= spec['quantity']
                
                line_item = OrderItem(
                    order_id=new_order.id,
                    product_id=product.id,
                    quantity=spec['quantity'],
                    unit_price_at_purchase=product.price
                )
                total += (product.price * spec['quantity'])
                session.add(line_item)
            
            new_order.total_amount = total
            session.add(new_order)
            session.commit()
            return new_order.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

def seed_initial_data(db: BicycleShopDatabase):
    
    session = db.get_session()
    if not session.query(Product).first():
        products = [
            Product(sku="TRK-DOM-001", name="Trek Domane SL 6", price=4299.99, stock_quantity=5, category="Road"),
            Product(sku="SPEC-STUMP-002", name="Specialized Stumpjumper", price=3500.00, stock_quantity=3, category="MTB"),
            Product(sku="CAN-TOP-003", name="Cannondale Topstone", price=1800.00, stock_quantity=10, category="Gravel")
        ]
        session.add_all(products)
        
        
        test_user = User(
            email="brad@example.com", 
            passkey_credential_id="cred_123456789",
            public_key="MCowBQYDK2VwAyEAGb..."
        )
        session.add(test_user)
        session.commit()
    session.close()

if __name__ == "__main__":
    
    shop_db = BicycleShopDatabase("sqlite:///bicycle_shop.db")
    seed_initial_data(shop_db)
    
    
    order_manager = OrderService(shop_db)
    
    
    with shop_db.get_session() as sess:
        user = sess.query(User).filter_by(email="brad@example.com").first()
        bike = sess.query(Product).filter_by(sku="TRK-DOM-001").first()
        
        if user and bike:
            try:
                order_id = order_manager.create_order(
                    user_id=user.id, 
                    item_specs=[{"product_id": bike.id, "quantity": 1}]
                )
                print(f"Order successfully created: {order_id}")
            except Exception as error:
                print(f"Transaction failed: {error}")