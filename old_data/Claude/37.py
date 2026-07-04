import sqlite3


conn = sqlite3.connect('bicycle_shop.db')
c = conn.cursor()


c.execute()

c.execute()

c.execute()


c.execute("INSERT INTO bikes VALUES (1, 'Mountain Bike', 'Trek', 'M', 599.99)")
c.execute("INSERT INTO bikes VALUES (2, 'Road Bike', 'Cannondale', 'L', 899.99)")
c.execute("INSERT INTO bikes VALUES (3, 'Hybrid Bike', 'Giant', 'S', 499.99)")

c.execute("INSERT INTO customers VALUES (1, 'John Doe', 'john@email.com', '555-1234')")
c.execute("INSERT INTO customers VALUES (2, 'Jane Smith', 'jane@email.com', '555-5678')")

c.execute("INSERT INTO orders VALUES (1, 1, 1, 1, 599.99, '2023-04-01')")
c.execute("INSERT INTO orders VALUES (2, 2, 2, 1, 899.99, '2023-04-15')")


conn.commit()
conn.close()