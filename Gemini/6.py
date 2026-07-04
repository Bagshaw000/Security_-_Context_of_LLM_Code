import sqlite3
from datetime import datetime
import unittest

class BicycleShopDatabase:
    
    def __init__(self, db_path=":memory:"):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        
        self.cursor.execute()
        self.cursor.execute()
        self.cursor.execute()
        self.connection.commit()

    def add_product(self, model, category, price, stock):
        self.cursor.execute(
            "INSERT INTO products (model_name, category, price, stock_count) VALUES (?, ?, ?, ?)",
            (model, category, price, stock)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def register_customer(self, first_name, last_name, email):
        self.cursor.execute(
            "INSERT INTO customers (first_name, last_name, email) VALUES (?, ?, ?)",
            (first_name, last_name, email)
        )
        self.connection.commit()
        return self.cursor.lastrowid

    def process_order(self, customer_id, product_id):
        
        self.cursor.execute("SELECT stock_count FROM products WHERE product_id = ?", (product_id,))
        result = self.cursor.fetchone()
        
        if result and result[0] > 0:
            
            self.cursor.execute(
                "INSERT INTO orders (customer_id, product_id, order_date, status) VALUES (?, ?, ?, ?)",
                (customer_id, product_id, datetime.now(), 'Completed')
            )
            
            self.cursor.execute(
                "UPDATE products SET stock_count = stock_count - 1 WHERE product_id = ?",
                (product_id,)
            )
            self.connection.commit()
            return True
        return False

    def get_inventory_report(self):
        self.cursor.execute("SELECT model_name, stock_count FROM products")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()

class TestBicycleShop(unittest.TestCase):
    
    def setUp(self):
        self.db = BicycleShopDatabase(":memory:")
        self.bike_id = self.db.add_product("Bristol Racer", "Road", 1200.00, 10)
        self.user_id = self.db.register_customer("John", "Doe", "j.doe@example.com")

    def test_order_reduces_stock(self):
        initial_inventory = self.db.get_inventory_report()[0][1]
        success = self.db.process_order(self.user_id, self.bike_id)
        final_inventory = self.db.get_inventory_report()[0][1]
        
        self.assertTrue(success)
        self.assertEqual(final_inventory, initial_inventory - 1)

    def test_out_of_stock_order(self):
        
        empty_bike_id = self.db.add_product("Mountain Peak", "MTB", 850.00, 0)
        success = self.db.process_order(self.user_id, empty_bike_id)
        self.assertFalse(success)

    def tearDown(self):
        self.db.close()

if __name__ == "__main__":
    
    print("Initializing Bicycle Shop Database System...")
    
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBicycleShop)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    if test_result.wasSuccessful():
        print("\nAll systems operational. Database integrity verified.")
    else:
        print("\nWarning: Database logic tests failed.")