import sqlite3
import unittest
from datetime import datetime

class BicycleShopDB:
    
    def __init__(self, db_name=":memory:"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_schema()

    def _create_schema(self):
        
        self.cursor.execute()
        self.cursor.execute()
        self.cursor.execute()
        self.conn.commit()

    def add_product(self, brand, model, category, price, stock):
        query = "INSERT INTO products (brand, model, category, price, stock_quantity) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (brand, model, category, price, stock))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_stock(self, product_id, quantity_change):
        
        query = "UPDATE products SET stock_quantity = stock_quantity + ? WHERE product_id = ?"
        self.cursor.execute(query, (quantity_change, product_id))
        self.conn.commit()

    def get_inventory_report(self):
        self.cursor.execute("SELECT brand, model, stock_quantity FROM products WHERE stock_quantity < 5")
        return self.cursor.fetchall()

    def register_customer(self, first_name, last_name, email):
        try:
            query = "INSERT INTO customers (first_name, last_name, email) VALUES (?, ?, ?)"
            self.cursor.execute(query, (first_name, last_name, email))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def close(self):
        self.conn.close()

class TestBicycleShopSystem(unittest.TestCase):
    
    def setUp(self):
        self.db = BicycleShopDB(":memory:")

    def test_product_insertion(self):
        product_id = self.db.add_product("Specialized", "Tarmac SL7", "Road", 5500.00, 10)
        self.db.cursor.execute("SELECT brand FROM products WHERE product_id = ?", (product_id,))
        brand = self.db.cursor.fetchone()[0]
        self.assertEqual(brand, "Specialized")

    def test_stock_management(self):
        product_id = self.db.add_product("Trek", "Fuel EX", "Mountain", 3200.00, 5)
        self.db.update_stock(product_id, -2)
        self.db.cursor.execute("SELECT stock_quantity FROM products WHERE product_id = ?", (product_id,))
        stock = self.db.cursor.fetchone()[0]
        self.assertEqual(stock, 3)

    def test_low_stock_report(self):
        self.db.add_product("Giant", "Defy", "Road", 2000.00, 2)
        self.db.add_product("Cannondale", "Topstone", "Gravel", 1800.00, 20)
        low_stock = self.db.get_inventory_report()
        self.assertEqual(len(low_stock), 1)
        self.assertEqual(low_stock[0][0], "Giant")

    def tearDown(self):
        self.db.close()

if __name__ == "__main__":
    
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

    
    shop = BicycleShopDB("bicycle_inventory.db")
    
    
    bike_1 = shop.add_product("Canyon", "Grizl", "Gravel", 2400.00, 8)
    bike_2 = shop.add_product("Santa Cruz", "Tallboy", "Mountain", 4500.00, 3)
    
    
    customer_id = shop.register_customer("Alice", "Smith", "alice.smith@example.com")
    
    
    if bike_2:
        shop.update_stock(bike_2, -1)
    
    print("Database processing complete. Low stock alerts generated for items under 5 units:")
    for item in shop.get_inventory_report():
        print(f"ALERT: {item[0]} {item[1]} is low on stock ({item[2]} remaining)")
    
    shop.close()