import uuid
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


product_category_association = Table(
    'product_category_link',
    Base.metadata,
    Column('product_id', String(36), ForeignKey('products.id')),
    Column('category_id', String(36), ForeignKey('categories.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    orders = relationship("Order", back_populates="user")

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone_number = Column(String(20))
    shipping_address = Column(Text)

    user = relationship("User", back_populates="profile")

class Category(Base):
    __tablename__ = 'categories'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)

    products = relationship("Product", secondary=product_category_association, back_populates="categories")

class Product(Base):
    __tablename__ = 'products'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sku = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    categories = relationship("Category", secondary=product_category_association, back_populates="products")

class Order(Base):
    __tablename__ = 'orders'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    status = Column(String(50), default='PENDING')  
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String(36), ForeignKey('orders.id'), nullable=False)
    product_id = Column(String(36), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class BicycleShopDatabase:
    
    def __init__(self, db_url: str = "sqlite:///bicycle_shop.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        return self.SessionLocal()

    def register_user(self, email: str, password_hash: str, first_name: str, last_name: str) -> User:
        with self.get_session() as session:
            user = User(email=email, password_hash=password_hash)
            profile = UserProfile(user=user, first_name=first_name, last_name=last_name)
            session.add(user)
            session.add(profile)
            session.commit()
            session.refresh(user)
            return user

    def add_product(self, sku: str, name: str, price: float, stock: int, categories: List[str] = None) -> Product:
        with self.get_session() as session:
            product = Product(sku=sku, name=name, price=price, stock_quantity=stock)
            if categories:
                for cat_name in categories:
                    category = session.query(Category).filter_by(name=cat_name).first()
                    if not category:
                        category = Category(name=cat_name)
                    product.categories.append(category)
            session.add(product)
            session.commit()
            session.refresh(product)
            return product

    def create_order(self, user_id: str, items: List[dict]) -> Order:
        
        with self.get_session() as session:
            total = 0.0
            order = Order(user_id=user_id, total_amount=0.0)
            session.add(order)
            
            for item_data in items:
                product = session.query(Product).filter_by(id=item_data['product_id']).one()
                if product.stock_quantity < item_data['quantity']:
                    raise ValueError(f"Insufficient stock for product {product.sku}")
                
                order_item = OrderItem(
                    order=order,
                    product_id=product.id,
                    quantity=item_data['quantity'],
                    unit_price=product.price
                )
                product.stock_quantity -= item_data['quantity']
                total += (product.price * item_data['quantity'])
                session.add(order_item)
            
            order.total_amount = total
            session.commit()
            session.refresh(order)
            return order

if __name__ == "__main__":
    
    shop_db = BicycleShopDatabase("sqlite:///:memory:")
    
    
    new_user = shop_db.register_user(
        email="customer@example.com", 
        password_hash="argon2$v=19$m=65536,t=3,p=4$hashed_string",
        first_name="Jane",
        last_name="Doe"
    )
    
    
    mountain_bike = shop_db.add_product(
        sku="MTB-001-RED",
        name="TrailBlazer 5000",
        price=1299.99,
        stock=10,
        categories=["Mountain", "Carbon Fiber"]
    )
    
    
    try:
        order = shop_db.create_order(
            user_id=new_user.id,
            items=[{"product_id": mountain_bike.id, "quantity": 1}]
        )
        print(f"Order created successfully: ID {order.id}, Total: ${order.total_amount}")
    except Exception as e:
        print(f"Failed to create order: {e}")