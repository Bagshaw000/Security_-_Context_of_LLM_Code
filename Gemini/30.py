import sqlite3
from dataclasses import dataclass
from datetime import datetime
import unittest

@dataclass
class Product:
    id: int
    model_name: str
    brand: str
    category: str
    price: float
    stock_level: int

class BicycleShopDatabase:
    
    def __init__(self, db_name=":memory:"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute()
        self.cursor.execute()
        self.connection.commit()

    def add_inventory(self, model_name, brand, category, price, stock_level):
        query = 
        self.cursor.execute(query, (model_name, brand, category, price, stock_level))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = self.cursor.fetchone()
        if row:
            return Product(*row)
        return None

    def update_stock(self, product_id, quantity_change):
        current_product = self.get_product_by_id(product_id)
        if not current_product:
            raise ValueError(f"Product ID {product_id} not found.")
        
        new_stock = current_product.stock_level + quantity_change
        if new_stock < 0:
            raise ValueError("Insufficient inventory to fulfill request.")
            
        self.cursor.execute("UPDATE products SET stock_level = ? WHERE id = ?", (new_stock, product_id))
        self.connection.commit()

    def place_order(self, product_id, customer_email, quantity):
        try:
            
            self.update_stock(product_id, -quantity)
            
            query = 
            self.cursor.execute(query, (product_id, customer_email, datetime.now(), quantity, 'PENDING'))
            self.connection.commit()
            return self.cursor.lastrowid
        except ValueError as e:
            print(f"Order failed: {e}")
            return None

    def close(self):
        self.connection.close()

class TestBicycleShopDB(unittest.TestCase):
    def setUp(self):
        
        self.db = BicycleShopDatabase(":memory:")
        self.test_bike_id = self.db.add_inventory("Allez Sprint", "Specialized", "Road", 2500.00, 10)

    def test_inventory_addition(self):
        product = self.db.get_product_by_id(self.test_bike_id)
        self.assertEqual(product.model_name, "Allez Sprint")
        self.assertEqual(product.stock_level, 10)

    def test_order_processing(self):
        order_id = self.db.place_order(self.test_bike_id, "customer@bristol.ac.uk", 2)
        self.assertIsNotNone(order_id)
        
        product = self.db.get_product_by_id(self.test_bike_id)
        self.assertEqual(product.stock_level, 8)

    def test_insufficient_stock(self):
        order_id = self.db.place_order(self.test_bike_id, "customer@bristol.ac.uk", 15)
        self.assertIsNone(order_id)
        
        product = self.db.get_product_by_id(self.test_bike_id)
        self.assertEqual(product.stock_level, 10)

    def tearDown(self):
        self.db.close()

if __name__ == "__main__":
    
    shop_db = BicycleShopDatabase("bicycle_shop_inventory.db")
    
    
    shop_db.add_inventory("Sirrus 2.0", "Specialized", "Hybrid", 650.00, 5)
    shop_db.add_inventory("Tarmac SL7", "Specialized", "Road", 5500.00, 3)
    
    print("Database system initialized. Running unit tests...")
    
    
    unittest.main(argv=['first-arg-is-ignored'], exit=False)