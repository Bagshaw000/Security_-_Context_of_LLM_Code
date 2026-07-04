import sqlite3
import unittest
from datetime import datetime
from typing import List, Tuple, Optional

class BicycleShopDatabase:
    
    def __init__(self, db_path: str = ":memory:"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        
        self.cursor.execute()
        
        self.cursor.execute()
        
        self.cursor.execute()
        self.connection.commit()

    def add_product(self, brand: str, model: str, material: str, price: float, stock: int) -> int:
        query = 
        self.cursor.execute(query, (brand, model, material, price, stock))
        self.connection.commit()
        return self.cursor.lastrowid

    def add_customer(self, first_name: str, last_name: str, email: str) -> int:
        query = "INSERT INTO customers (first_name, last_name, email) VALUES (?, ?, ?)"
        self.cursor.execute(query, (first_name, last_name, email))
        self.connection.commit()
        return self.cursor.lastrowid

    def process_order(self, customer_id: int, product_id: int) -> bool:
        
        
        self.cursor.execute("SELECT quantity_in_stock FROM products WHERE product_id = ?", (product_id,))
        result = self.cursor.fetchone()
        
        if result and result[0] > 0:
            
            self.cursor.execute(
                "UPDATE products SET quantity_in_stock = quantity_in_stock - 1 WHERE product_id = ?", 
                (product_id,)
            )
            
            
            self.cursor.execute(
                "INSERT INTO orders (customer_id, product_id, order_date) VALUES (?, ?, ?)",
                (customer_id, product_id, datetime.now())
            )
            self.connection.commit()
            return True
        return False

    def get_inventory_levels(self) -> List[Tuple]:
        self.cursor.execute("SELECT brand, model, quantity_in_stock FROM products")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

class TestBicycleShop(unittest.TestCase):
    
    def setUp(self):
        self.db = BicycleShopDatabase(":memory:")
        self.product_id = self.db.add_product("Specialized", "Allez", "Aluminium", 1100.00, 5)
        self.customer_id = self.db.add_customer("John", "Doe", "john.doe@bristol.ac.uk")

    def test_inventory_reduction(self):
        
        initial_stock = self.db.get_inventory_levels()[0][2]
        self.assertEqual(initial_stock, 5)
        
        
        success = self.db.process_order(self.customer_id, self.product_id)
        self.assertTrue(success)
        
        
        new_stock = self.db.get_inventory_levels()[0][2]
        self.assertEqual(new_stock, 4)

    def test_out_of_stock_failure(self):
        
        empty_bike_id = self.db.add_product("Cannondale", "CAAD13", "Aluminium", 1800.00, 0)
        success = self.db.process_order(self.customer_id, empty_bike_id)
        self.assertFalse(success)

    def tearDown(self):
        self.db.close()

if __name__ == "__main__":
    
    shop_db = BicycleShopDatabase("online_shop.db")
    
    
    shop_db.add_product("Trek", "Domane", "Carbon", 2500.00, 10)
    shop_db.add_product("Giant", "Defy", "Carbon", 2200.00, 8)
    
    print("Database initialized and seeded.")
    
    
    print("Running system validation tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBicycleShop)
    unittest.TextTestRunner(verbosity=2).run(suite)