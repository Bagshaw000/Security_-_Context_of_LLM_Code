

import sqlite3


conn = sqlite3.connect('bicycle_shop.db')


c = conn.cursor()


c.execute()


c.execute()


c.execute()


c.execute("INSERT INTO Bicycles (model, brand, price, quantity) VALUES ('Mountain Bike', 'Trek', 799.99, 20)")
c.execute("INSERT INTO Bicycles (model, brand, price, quantity) VALUES ('Road Bike', 'Specialized', 1199.99, 15)")
c.execute("INSERT INTO Customers (name, email, phone) VALUES ('John Doe', 'john.doe@email.com', '555-1234')")
c.execute("INSERT INTO Customers (name, email, phone) VALUES ('Jane Smith', 'jane.smith@email.com', '555-5678')")
c.execute("INSERT INTO Orders (customer_id, bicycle_id, quantity, total, order_date) VALUES (1, 1, 1, 799.99, '2023-04-15')")
c.execute("INSERT INTO Orders (customer_id, bicycle_id, quantity, total, order_date) VALUES (2, 2, 1, 1199.99, '2023-04-20')")


conn.commit()
conn.close()