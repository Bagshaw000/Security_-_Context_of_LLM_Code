import sqlite3
import hashlib
import uuid
import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum, auto


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BicycleShopDB")

class OrderStatus(Enum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()

@dataclass
class User:
    user_id: str
    email: str
    password_hash: str
    created_at: datetime
    is_active: bool = True

@dataclass
class Product:
    sku: str
    name: str
    brand: str
    price: float
    stock_quantity: int
    category: str

@dataclass
class Order:
    order_id: str
    user_id: str
    items: List[Dict[str, Any]]
    total_amount: float
    status: OrderStatus
    timestamp: datetime

class DatabaseSchema:
    
    
    CREATE_USERS_TABLE = 

    CREATE_PRODUCTS_TABLE = 

    CREATE_ORDERS_TABLE = 

    CREATE_ORDER_ITEMS_TABLE = 

class BicycleShopRepository:
    

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DatabaseSchema.CREATE_USERS_TABLE)
            cursor.execute(DatabaseSchema.CREATE_PRODUCTS_TABLE)
            cursor.execute(DatabaseSchema.CREATE_ORDERS_TABLE)
            cursor.execute(DatabaseSchema.CREATE_ORDER_ITEMS_TABLE)
            conn.commit()

    

    def create_user(self, email: str, password_raw: str) -> str:
        user_id = str(uuid.uuid4())
        password_hash = hashlib.sha256(password_raw.encode()).hexdigest()
        created_at = datetime.now()
        
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "INSERT INTO users (user_id, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                    (user_id, email, password_hash, created_at)
                )
            return user_id
        except sqlite3.IntegrityError:
            logger.error(f"User with email {email} already exists.")
            raise ValueError("User registration failed: Email exists.")

    def get_user_by_email(self, email: str) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return User(*row)
        return None

    

    def add_product(self, product: Product):
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO products (sku, name, brand, price, stock_quantity, category) VALUES (?, ?, ?, ?, ?, ?)",
                (product.sku, product.name, product.brand, product.price, product.stock_quantity, product.category)
            )

    def update_stock(self, sku: str, quantity_delta: int):
        
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE products SET stock_quantity = stock_quantity + ? WHERE sku = ?",
                (quantity_delta, sku)
            )

    def get_product(self, sku: str) -> Optional[Product]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM products WHERE sku = ?", (sku,))
            row = cursor.fetchone()
            return Product(*row) if row else None

    

    def place_order(self, user_id: str, items: List[Dict[str, Any]]) -> str:
        
        order_id = str(uuid.uuid4())
        timestamp = datetime.now()
        total_amount = 0.0

        with self._get_connection() as conn:
            conn.execute("BEGIN TRANSACTION")
            try:
                
                for item in items:
                    cursor = conn.execute("SELECT price, stock_quantity FROM products WHERE sku = ?", (item['sku'],))
                    res = cursor.fetchone()
                    if not res or res[1] < item['quantity']:
                        raise Exception(f"Insufficient stock for SKU: {item['sku']}")
                    
                    price = res[0]
                    total_amount += price * item['quantity']
                    item['unit_price'] = price

                
                conn.execute(
                    "INSERT INTO orders (order_id, user_id, total_amount, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (order_id, user_id, total_amount, OrderStatus.PENDING.name, timestamp)
                )

                
                for item in items:
                    conn.execute(
                        "INSERT INTO order_items (order_id, sku, quantity, unit_price) VALUES (?, ?, ?, ?)",
                        (order_id, item['sku'], item['quantity'], item['unit_price'])
                    )
                    conn.execute(
                        "UPDATE products SET stock_quantity = stock_quantity - ? WHERE sku = ?",
                        (item['quantity'], item['sku'])
                    )

                conn.commit()
                logger.info(f"Order {order_id} placed successfully for user {user_id}.")
                return order_id
            except Exception as e:
                conn.rollback()
                logger.error(f"Order failed: {str(e)}")
                raise



class BicycleShopService:
    def __init__(self, repository: BicycleShopRepository):
        self.repo = repository

    def register_customer(self, email: str, password: str):
        return self.repo.create_user(email, password)

    def bootstrap_inventory(self):
        bikes = [
            Product("BK-001", "Roadmaster 5000", "Specialized", 1200.00, 10, "Road"),
            Product("BK-002", "Mountain Peak", "Trek", 850.00, 5, "MTB"),
            Product("BK-003", "City Slicker", "Giant", 450.00, 15, "Hybrid")
        ]
        for bike in bikes:
            try:
                self.repo.add_product(bike)
            except sqlite3.IntegrityError:
                pass

    def purchase_bicycle(self, user_id: str, sku: str, quantity: int):
        return self.repo.place_order(user_id, [{"sku": sku, "quantity": quantity}])



if __name__ == "__main__":
    
    repo = BicycleShopRepository(":memory:")
    service = BicycleShopService(repo)
    service.bootstrap_inventory()

    
    try:
        user_uuid = service.register_customer("brad@amazon.com", "secure_passkey_2024")
        print(f"User created with ID: {user_uuid}")
    except ValueError as e:
        print(e)

    
    product = repo.get_product("BK-001")
    print(f"Product: {product.name}, Stock: {product.stock_quantity}")

    
    try:
        order_id = service.purchase_bicycle(user_uuid, "BK-001", 1)
        print(f"Order successful! ID: {order_id}")
    except Exception as e:
        print(f"Purchase failed: {e}")

    
    product_after = repo.get_product("BK-001")
    print(f"Product: {product_after.name}, Stock Remaining: {product_after.stock_quantity}")