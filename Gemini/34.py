import sqlite3
import unittest
from datetime import datetime

class BicycleInventoryManager:
    
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._initialize_schema()

    def _initialize_schema(self):
        
        self.cursor.execute()
        
        
        self.cursor.execute()
        self.conn.commit()

    def add_new_bicycle(self, brand, model, frame_type, price, initial_stock):
        query = 
        self.cursor.execute(query, (brand, model, frame_type, price, initial_stock))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_stock_level(self, bicycle_id, new_quantity):
        query = "UPDATE inventory SET quantity_in_stock = ? WHERE bicycle_id = ?"
        self.cursor.execute(query, (new_quantity, bicycle_id))
        self.conn.commit()

    def get_bicycle_details(self, bicycle_id):
        query = "SELECT * FROM inventory WHERE bicycle_id = ?"
        self.cursor.execute(query, (bicycle_id,))
        return self.cursor.fetchone()

    def place_order(self, bicycle_id, customer_name, quantity):
        
        self.cursor.execute("SELECT quantity_in_stock FROM inventory WHERE bicycle_id = ?", (bicycle_id,))
        result = self.cursor.fetchone()
        
        if not result:
            raise ValueError("Bicycle ID not found in inventory.")
        
        current_stock = result[0]
        if current_stock < quantity:
            return False, "Insufficient stock available."

        
        new_stock = current_stock - quantity
        self.update_stock_level(bicycle_id, new_stock)

        
        order_query = 
        self.cursor.execute(order_query, (bicycle_id, customer_name, quantity, datetime.now()))
        self.conn.commit()
        
        return True, "Order placed successfully."

class TestBicycleShopDB(unittest.TestCase):
    
    def setUp(self):
        
        self.manager = BicycleInventoryManager(":memory:")
        self.test_bike_id = self.manager.add_new_bicycle("Canyon", "Ultimate CF SLX", "Road", 6500.00, 5)

    def test_initial_stock(self):
        bike = self.manager.get_bicycle_details(self.test_bike_id)
        self.assertEqual(bike[5], 5) 

    def test_successful_order(self):
        success, message = self.manager.place_order(self.test_bike_id, "Alice Smith", 2)
        self.assertTrue(success)
        bike = self.manager.get_bicycle_details(self.test_bike_id)
        self.assertEqual(bike[5], 3)

    def test_failed_order_due_to_stock(self):
        success, message = self.manager.place_order(self.test_bike_id, "Bob Jones", 10)
        self.assertFalse(success)
        self.assertEqual(message, "Insufficient stock available.")
        bike = self.manager.get_bicycle_details(self.test_bike_id)
        self.assertEqual(bike[5], 5)

if __name__ == "__main__":
    
    print("Initializing Online Bicycle Shop Database System...")
    
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBicycleShopDB)
    unittest.TextTestRunner(verbosity=2).run(suite)

    
    shop_db = BicycleInventoryManager("bicycle_shop_prod.db")
    shop_db.add_new_bicycle("Brompton", "C Line", "Folding", 1250.00, 12)
    shop_db.add_new_bicycle("Specialized", "Sirrus", "Hybrid", 850.00, 20)
    
    print("\nInventory seeded in bicycle_shop_prod.db")
    current_bikes = shop_db.cursor.execute("SELECT brand, model, quantity_in_stock FROM inventory").fetchall()
    for bike in current_bikes:
        print(f"Stock: {bike[0]} {bike[1]} - {bike[2]} units")