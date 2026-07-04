
import sqlite3

class BicycleShopDatabase:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute()

        self.cursor.execute()

        self.cursor.execute()

        self.conn.commit()

    def insert_customer(self, name, email):
        self.cursor.execute('INSERT INTO customers (name, email) VALUES (?, ?)', (name, email))
        self.conn.commit()

    def get_customers(self):
        self.cursor.execute('SELECT * FROM customers')
        return self.cursor.fetchall()

    def insert_product(self, name, description, price):
        self.cursor.execute('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', (name, description, price))
        self.conn.commit()

    def get_products(self):
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()

    def insert_order(self, customer_id, product_id, quantity, total_price):
        self.cursor.execute('INSERT INTO orders (customer_id, product_id, quantity, total_price) VALUES (?, ?, ?, ?)', (customer_id, product_id, quantity, total_price))
        self.conn.commit()

    def get_orders(self):
        self.cursor.execute('SELECT * FROM orders')
        return self.cursor.fetchall()


db = BicycleShopDatabase('bicycle_shop.db')


db.insert_customer('John Doe', 'john@example.com')
print(db.get_customers())

db.insert_product('Road Bike', 'A high-performance road bike.', 1000.0)
print(db.get_products())

db.insert_order(1, 1, 2, 2000.0)
print(db.get_orders())
