import sqlite3


conn = sqlite3.connect('bicycle_shop.db')
c = conn.cursor()


c.execute()

c.execute()

c.execute()


c.execute("INSERT INTO customers (name, email, phone) VALUES ('John Doe', 'john@email.com', '555-1234')")
c.execute("INSERT INTO customers (name, email, phone) VALUES ('Jane Smith', 'jane@email.com', '555-5678')")

c.execute("INSERT INTO bikes (model, brand, price, in_stock) VALUES ('Mountain Bike', 'Trek', 599.99, 10)")
c.execute("INSERT INTO bikes (model, brand, price, in_stock) VALUES ('Road Bike', 'Specialized', 899.99, 5)")

c.execute("INSERT INTO orders (customer_id, bike_id, quantity, total_price, order_date) VALUES (1, 1, 1, 599.99, '2023-04-01')")
c.execute("INSERT INTO orders (customer_id, bike_id, quantity, total_price, order_date) VALUES (2, 2, 2, 1799.98, '2023-04-15')")


conn.commit()
conn.close()