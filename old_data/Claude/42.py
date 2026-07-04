import sqlite3


conn = sqlite3.connect('bicycle_shop.db')
c = conn.cursor()


c.execute()

c.execute()

c.execute()


c.execute("INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)", ("Mountain Bike", "High-performance mountain bike", 599.99, 10))
c.execute("INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)", ("Road Bike", "Lightweight road bike", 799.99, 15))
c.execute("INSERT INTO products (name, description, price, quantity) VALUES (?, ?, ?, ?)", ("BMX Bike", "Freestyle BMX bike", 299.99, 8))

c.execute("INSERT INTO orders (customer_name, customer_email, order_date, total_price) VALUES (?, ?, ?, ?)", ("John Doe", "john.doe@example.com", "2023-04-01", 599.99))
c.execute("INSERT INTO orders (customer_name, customer_email, order_date, total_price) VALUES (?, ?, ?, ?)", ("Jane Smith", "jane.smith@example.com", "2023-04-02", 799.99))

c.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", (1, 1, 1))
c.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)", (2, 2, 1))


conn.commit()
conn.close()