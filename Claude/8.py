import sqlite3


conn = sqlite3.connect('bicycle_shop.db')
c = conn.cursor()


c.execute()

c.execute()

c.execute()


c.execute("INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)", ("Mountain Bike", "High-quality mountain bike", 499.99, 10))
c.execute("INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)", ("Road Bike", "Lightweight road bike", 699.99, 5))
c.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", ("John Doe", "john@example.com", "555-1234"))
c.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", ("Jane Smith", "jane@example.com", "555-5678"))
c.execute("INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)", (1, 1, 1, "2023-04-15"))
c.execute("INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)", (2, 2, 2, "2023-04-20"))


conn.commit()
conn.close()